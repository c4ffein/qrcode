#!/usr/bin/env python3
"""
QRCode Library Bundler

This script consolidates the entire python-qrcode library into a single Python file
by parsing all modules into ASTs and resolving dependencies.

Copyright (c) 2025 c4ffein
Licensed under the MIT License - see LICENSE file for details
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class ImportAnalyzer(ast.NodeVisitor):
    """Analyzes imports in an AST to determine dependencies."""

    def __init__(self, module_name: str):
        self.module_name = module_name
        self.imports = set()
        self.from_imports = defaultdict(set)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.startswith('qrcode'):
                self.imports.add(alias.name)

    def visit_ImportFrom(self, node):
        if node.module and node.module.startswith('qrcode'):
            for alias in node.names:
                self.from_imports[node.module].add(alias.name)


class QRCodeConsolidator:
    """Main consolidator class that handles the entire process."""

    def __init__(self, qrcode_path: str):
        self.qrcode_path = Path(qrcode_path)
        self.modules = {}  # module_name -> AST
        self.dependencies = defaultdict(set)  # module -> set of dependencies
        self.module_paths = {}  # module_name -> file_path

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the qrcode directory."""
        python_files = []
        for root, dirs, files in os.walk(self.qrcode_path):
            # Skip __pycache__ and tests
            dirs[:] = [d for d in dirs if d not in ('__pycache__', 'tests')]
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        return python_files

    def path_to_module_name(self, file_path: Path) -> str:
        """Convert a file path to a module name."""
        # Get relative path from qrcode directory
        rel_path = file_path.relative_to(self.qrcode_path.parent)

        # Convert path to module name
        parts = list(rel_path.parts)
        if parts[-1] == '__init__.py':
            parts = parts[:-1]
        elif parts[-1].endswith('.py'):
            parts[-1] = parts[-1][:-3]

        return '.'.join(parts)

    def load_and_parse_files(self):
        """Load and parse all Python files into ASTs."""
        python_files = self.find_python_files()
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                tree = ast.parse(content)
                module_name = self.path_to_module_name(file_path)
                self.modules[module_name] = tree
                self.module_paths[module_name] = file_path
                # Analyze dependencies
                analyzer = ImportAnalyzer(module_name)
                analyzer.visit(tree)
                # Add dependencies
                for imp in analyzer.imports:
                    if imp in self.modules or imp.startswith('qrcode'):
                        self.dependencies[module_name].add(imp)
                for module, names in analyzer.from_imports.items():
                    if module.startswith('qrcode'):
                        self.dependencies[module_name].add(module)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    def remove_type_checking_blocks(self, tree: ast.AST) -> ast.AST:
        """Remove TYPE_CHECKING blocks from AST."""
        class TypeCheckingRemover(ast.NodeTransformer):
            def visit_If(self, node):
                # Remove TYPE_CHECKING blocks
                if (isinstance(node.test, ast.Name) and
                    node.test.id == 'TYPE_CHECKING'):
                    return None
                return self.generic_visit(node)

        return TypeCheckingRemover().visit(tree)

    def dependency_order_from_imports(self) -> List[str]:
        """
        Determine module order based on the natural order of imports encountered.
        Walk through all modules and build dependency order from import statements.
        """
        ordered_modules = []
        processed = set()
        # Track what each module imports
        import_graph = {}
        for module_name, tree in self.modules.items():
            # Remove TYPE_CHECKING blocks before analyzing dependencies
            clean_tree = self.remove_type_checking_blocks(tree)
            imports = set()
            for node in ast.walk(clean_tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith('qrcode'):
                            imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith('qrcode') and node.level == 0:
                        # Handle "from qrcode import util, constants" - add submodules
                        base_module = node.module
                        for alias in node.names:
                            # Check if this is importing a submodule (e.g., util, constants)
                            potential_submodule = f"{base_module}.{alias.name}"
                            if potential_submodule in self.modules:
                                imports.add(potential_submodule)
                            else:
                                # It's importing from the module itself
                                imports.add(base_module)
                    elif node.level > 0:  # relative import
                        # Convert relative import to absolute
                        parts = module_name.split('.')
                        if node.level == 1 and node.module:
                            # from .module import X
                            rel_module = '.'.join(parts[:-1] + [node.module])
                            imports.add(rel_module)
                        elif node.level == 1 and not node.module:
                            # from . import X - imports from parent package
                            for alias in node.names:
                                # Check if importing submodules
                                potential_submodule = '.'.join(parts[:-1] + [alias.name])
                                if potential_submodule in self.modules:
                                    imports.add(potential_submodule)
                                else:
                                    imports.add('.'.join(parts[:-1]))
            import_graph[module_name] = imports
        # Process modules with simple DFS
        def add_module(module_name):
            # Skip if already processed or not in our modules
            if module_name in processed or module_name not in self.modules:
                return

            # Mark as processed immediately (prevents infinite loops)
            processed.add(module_name)

            # First, recursively add all dependencies that haven't been processed
            # Sort dependencies for deterministic ordering
            for dep in sorted(import_graph.get(module_name, set())):
                if dep in self.modules and dep not in processed:
                    add_module(dep)

            # Then add this module to the ordered list
            ordered_modules.append(module_name)

        # Process all modules in DFS order based on dependencies
        # Sort module names to ensure deterministic output
        for module_name in sorted(self.modules.keys()):
            add_module(module_name)
        return ordered_modules

    def build_global_symbol_table(self) -> Dict[str, str]:
        """Build a global symbol table mapping all names to avoid forward references."""
        symbol_table = {}

        for module_name, tree in self.modules.items():
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    symbol_table[node.name] = node.name
                elif isinstance(node, ast.FunctionDef):
                    symbol_table[node.name] = node.name
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            symbol_table[target.id] = target.id
        return symbol_table

    def remove_qrcode_imports(self, tree: ast.AST, module_name: str = '') -> ast.AST:
        """Remove qrcode-internal imports from an AST."""
        class ImportRemover(ast.NodeTransformer):
            def __init__(self, module_name):
                self.module_name = module_name

            def visit_FunctionDef(self, node):
                # Remove @deprecation decorators
                node.decorator_list = [d for d in node.decorator_list
                                      if not (isinstance(d, ast.Call) and
                                            isinstance(d.func, ast.Attribute) and
                                            isinstance(d.func.value, ast.Name) and
                                            d.func.value.id == 'deprecation')]
                return self.generic_visit(node)

            def visit_Import(self, node):
                node.names = [alias for alias in node.names
                            if not alias.name.startswith('qrcode')]
                return node if node.names else None

            def visit_ImportFrom(self, node):
                # Remove qrcode imports and relative imports (level > 0)
                if (node.module and node.module.startswith('qrcode')) or node.level > 0:
                    return None
                return node

            def visit_If(self, node):
                # Handle TYPE_CHECKING blocks - remove qrcode imports inside them
                # but preserve the structure
                if (isinstance(node.test, ast.Name) and
                    node.test.id == 'TYPE_CHECKING'):
                    # Filter out qrcode imports from the TYPE_CHECKING block
                    new_body = []
                    for stmt in node.body:
                        if isinstance(stmt, ast.ImportFrom):
                            if not (stmt.module and stmt.module.startswith('qrcode')):
                                new_body.append(stmt)
                        elif isinstance(stmt, ast.Import):
                            stmt.names = [alias for alias in stmt.names
                                        if not alias.name.startswith('qrcode')]
                            if stmt.names:
                                new_body.append(stmt)
                        else:
                            new_body.append(stmt)

                    # If the TYPE_CHECKING block becomes empty, remove it entirely
                    if not new_body:
                        return None

                    node.body = new_body
                    return node

                # Remove all if __name__ == "__main__" blocks
                # (We'll keep console_scripts as the entry point)
                if (isinstance(node.test, ast.Compare) and
                    isinstance(node.test.left, ast.Name) and
                    node.test.left.id == '__name__' and
                    len(node.test.ops) == 1 and
                    isinstance(node.test.ops[0], ast.Eq) and
                    len(node.test.comparators) == 1 and
                    isinstance(node.test.comparators[0], ast.Constant) and
                    node.test.comparators[0].value == '__main__'):
                    return None

                # For other if statements, continue normal processing
                return self.generic_visit(node)

        # Transform references to use global names
        class ReferenceTransformer(ast.NodeTransformer):
            def __init__(self, symbol_table):
                self.symbol_table = symbol_table

            def visit_Attribute(self, node):
                # Handle qrcode module references
                if self._is_qrcode_reference(node):
                    # Check if the final attribute is in our symbol table
                    if node.attr in self.symbol_table:
                        return ast.Name(id=node.attr, ctx=node.ctx)
                return self.generic_visit(node)

            def visit_Name(self, node):
                # Handle simple name references that might need resolving
                if isinstance(node.ctx, ast.Load) and node.id in self.symbol_table:
                    # Reference is valid in global scope
                    return node
                return node

            def _is_qrcode_reference(self, node):
                """Check if this is a reference to a qrcode module."""
                if isinstance(node.value, ast.Name):
                    # Simple case: base.BaseImage, constants.X, etc.
                    return node.value.id in ['constants', 'exceptions', 'util', 'base', 'image']
                elif isinstance(node.value, ast.Attribute):
                    # Nested case: qrcode.image.base.BaseImage
                    current = node.value
                    while isinstance(current, ast.Attribute):
                        current = current.value
                    # Check if the root is 'qrcode'
                    return isinstance(current, ast.Name) and current.id == 'qrcode'
                return False

        clean_tree = ImportRemover(module_name).visit(tree)
        return clean_tree  # Symbol table will be applied globally later

    def collect_external_imports(self) -> Dict[str, Set[str]]:
        """Collect all external (non-qrcode) imports, excluding known optional dependencies."""
        stdlib_imports = set()
        from_imports = defaultdict(set)

        # Known optional/problematic imports that should be handled within modules
        excluded_imports = {'png', 'PIL', 'colorama', 'lxml.etree', 'deprecation', 'lxml'}

        for tree in self.modules.values():
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if (not alias.name.startswith('qrcode') and
                            alias.name not in excluded_imports):
                            stdlib_imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    # Skip relative imports (level > 0) and qrcode imports
                    if (node.module and
                        not node.module.startswith('qrcode') and
                        node.level == 0 and
                        node.module not in excluded_imports):
                        for alias in node.names:
                            from_imports[node.module].add(alias.name)

        return {'stdlib': stdlib_imports, 'from': from_imports}

    def sort_module_content(self, tree: ast.AST) -> ast.AST:
        """Sort the content within a module by dependencies."""
        if not isinstance(tree, ast.Module):
            return tree

        # Separate different types of statements
        imports = []
        classes = []
        functions = []
        variables = []
        type_definitions = []  # TypeVar, type aliases, etc.
        other = []

        # Build dependency graph for classes, functions, and variables within this module
        class_deps = defaultdict(set)
        func_deps = defaultdict(set)
        var_deps = defaultdict(set)
        var_names = {}  # Map variable names to their nodes

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(node)
            elif isinstance(node, ast.ClassDef):
                classes.append(node)
                # Find what this class depends on
                for child in ast.walk(node):
                    if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                        class_deps[node.name].add(child.id)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node)
                # Find what this function depends on
                for child in ast.walk(node):
                    if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                        func_deps[node.name].add(child.id)
            elif isinstance(node, ast.Assign):
                # Check if this is a type definition (TypeVar, etc.)
                is_type_def = False
                if (hasattr(node, 'value') and isinstance(node.value, ast.Call) and
                    isinstance(node.value.func, ast.Name)):
                    func_name = node.value.func.id
                    if func_name in ['TypeVar', 'type', 'NewType']:
                        is_type_def = True

                if is_type_def:
                    type_definitions.append(node)
                else:
                    variables.append(node)
                    # Track dependencies for variables
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_names[target.id] = node
                            # Find what this variable depends on
                            for child in ast.walk(node.value):
                                if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                                    var_deps[target.id].add(child.id)
            else:
                other.append(node)

        # Sort classes by dependencies
        def sort_by_deps(items, deps_dict):
            sorted_items = []
            processed = set()
            visiting = set()  # Cycle detection

            def add_item(item):
                name = item.name if hasattr(item, 'name') else str(item)
                if name in processed:
                    return

                if name in visiting:
                    # Cycle detected, skip
                    return

                visiting.add(name)

                # Add dependencies first (only if they exist in this module)
                deps = deps_dict.get(name, set())
                for dep in deps:
                    # Find the item with this name
                    for candidate in items:
                        if hasattr(candidate, 'name') and candidate.name == dep:
                            if dep not in processed and dep not in visiting:
                                add_item(candidate)

                # Add this item
                if name not in processed:
                    sorted_items.append(item)
                    processed.add(name)

                visiting.discard(name)

            for item in items:
                add_item(item)

            return sorted_items

        sorted_classes = sort_by_deps(classes, class_deps)
        sorted_functions = sort_by_deps(functions, func_deps)

        # Sort everything more carefully - classes first, then variables that reference them
        sorted_variables = []
        processed_vars = set()

        def add_variable(var_node):
            if var_node in processed_vars:
                return

            # Check if this variable references any classes
            for node in ast.walk(var_node):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    # If this references a class, make sure the class comes first
                    for class_node in sorted_classes:
                        if class_node.name == node.id:
                            # This variable references a class, so it should come after classes
                            break

            sorted_variables.append(var_node)
            processed_vars.add(var_node)

        for var in variables:
            add_variable(var)

        # Rebuild the module: imports, then type definitions, then classes, then variables, then functions, then other
        new_body = imports + type_definitions + sorted_classes + sorted_variables + sorted_functions + other
        tree.body = new_body
        return tree

    def generate_consolidated_file(self, output_path: str = 'qrcode.py'):
        """Generate the consolidated Python file."""
        print("Loading and parsing files...")
        self.load_and_parse_files()

        print("Sorting modules by import dependencies...")
        sorted_modules = self.dependency_order_from_imports()
        print(f"Module order ({len(sorted_modules)} modules):")
        for i, module in enumerate(sorted_modules, 1):
            print(f"  {i}. {module}")

        print("\nCollecting external imports...")
        imports_info = self.collect_external_imports()

        print("Building global symbol table...")
        global_symbols = self.build_global_symbol_table()

        print(f"Generating consolidated file: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header with license information
            f.write('"""\n')
            f.write('Consolidated QRCode Library\n')
            f.write('\n')
            f.write('Generated automatically from python-qrcode using bundler.py\n')
            f.write('All internal imports have been resolved and removed.\n')
            f.write('\n')
            f.write('This is a derivative work of python-qrcode:\n')
            f.write('https://github.com/lincolnloop/python-qrcode\n')
            f.write('\n')

            # Include the original license
            license_path = self.qrcode_path.parent / 'LICENSE'
            if license_path.exists():
                f.write('Original LICENSE:\n')
                f.write('-' * 78 + '\n')
                with open(license_path, 'r', encoding='utf-8') as license_file:
                    f.write(license_file.read())
                f.write('-' * 78 + '\n')

            f.write('"""\n\n')

            # Write __future__ imports first
            future_imports = {imp for imp in imports_info['from'].get('__future__', set())}
            if future_imports:
                for imp in sorted(future_imports):
                    f.write(f"from __future__ import {imp}\n")
                f.write("\n")

            # Write standard library imports
            for imp in sorted(imports_info['stdlib']):
                f.write(f"import {imp}\n")

            if imports_info['stdlib']:
                f.write("\n")

            # Write from imports (excluding __future__)
            for module, names in sorted(imports_info['from'].items()):
                if module != '__future__':
                    for name in sorted(names):
                        f.write(f"from {module} import {name}\n")

            f.write("\n\n")
            # Add try/except for optional dependencies
            f.write("# Optional dependencies (may not be installed)\n")
            f.write("try:\n")
            f.write("    from PIL import Image, ImageDraw\n")
            f.write("except ImportError:\n")
            f.write("    Image = None\n")
            f.write("    ImageDraw = None\n\n")
            f.write("# Patch metadata.version to handle missing package metadata\n")
            f.write("_original_metadata_version = metadata.version\n")
            f.write("def _patched_metadata_version(name):\n")
            f.write("    try:\n")
            f.write("        return _original_metadata_version(name)\n")
            f.write("    except Exception:\n")
            f.write("        return 'consolidated'\n")
            f.write("metadata.version = _patched_metadata_version\n\n")
            # Write namespace class for module references
            f.write("# Namespace class to hold module-level definitions\n")
            f.write("class _ModuleNamespace:\n")
            f.write("    pass\n\n")

            # Build all parent namespace hierarchies from modules
            f.write("# Create namespace hierarchy\n")
            created_namespaces = set()
            for module_name in sorted_modules:
                parts = module_name.split('.')
                # Create all parent namespaces
                for i in range(len(parts)):
                    namespace_path = '.'.join(parts[:i+1])
                    if namespace_path not in created_namespaces:
                        created_namespaces.add(namespace_path)
                        if i == 0:
                            # Root level (e.g., "qrcode")
                            f.write(f"{namespace_path} = _ModuleNamespace()\n")
                        else:
                            # Nested level (e.g., "qrcode.image")
                            parent = '.'.join(parts[:i])
                            child = parts[i]
                            f.write(f"{parent}.{child} = _ModuleNamespace()\n")
            f.write("\n")

            # Create short name aliases upfront to avoid ordering issues
            # Prioritize top-level qrcode.* modules over nested ones
            f.write("# Create short name aliases for common module references\n")
            short_name_mapping = {}
            for module_name in sorted_modules:
                if module_name.startswith('qrcode.') and module_name.count('.') == 1:
                    # Top-level qrcode modules like qrcode.constants, qrcode.base
                    short_name = module_name.split('.')[-1]
                    if short_name not in ['__init__', '__main__']:
                        short_name_mapping[short_name] = module_name

            # Add special aliases for nested modules that are commonly used
            if 'qrcode.image.styles.moduledrawers.svg' in sorted_modules:
                short_name_mapping['svg_drawers'] = 'qrcode.image.styles.moduledrawers.svg'

            for short_name, full_name in short_name_mapping.items():
                f.write(f"{short_name} = {full_name}\n")
            f.write("\n")

            # Write each module's content
            module_exports = {}  # Track what each module exports
            used_short_names = set()  # Track short names to avoid conflicts
            for i, module_name in enumerate(sorted_modules):
                # Skip __main__ module since it just calls main() which we'll add at the end
                if module_name == 'qrcode.__main__':
                    continue

                tree = self.modules[module_name]

                # Remove qrcode imports
                clean_tree = self.remove_qrcode_imports(tree, module_name)

                # Add module comment
                f.write(f"# " + "="*60 + "\n")
                f.write(f"# Module: {module_name}\n")
                f.write(f"# Original: {self.module_paths[module_name]}\n")
                f.write(f"# " + "="*60 + "\n\n")

                # Convert AST back to code
                try:
                    # Remove import statements from the beginning of each module
                    class ImportStripper(ast.NodeTransformer):
                        def visit_Module(self, node):
                            # Filter out all import statements at module level
                            new_body = []
                            for stmt in node.body:
                                if not isinstance(stmt, (ast.Import, ast.ImportFrom)):
                                    new_body.append(stmt)
                            node.body = new_body
                            return node

                    stripped_tree = ImportStripper().visit(clean_tree)

                    # Collect exports from this module
                    exports = []
                    for node in stripped_tree.body:
                        if isinstance(node, ast.ClassDef):
                            exports.append(node.name)
                        elif isinstance(node, ast.FunctionDef):
                            exports.append(node.name)
                        elif isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    exports.append(target.id)

                    module_exports[module_name] = exports

                    # Don't transform references - keep them as-is to avoid name conflicts
                    code = ast.unparse(stripped_tree)
                    f.write(code)
                    f.write("\n\n")

                    # Populate the namespace with exports
                    if exports:
                        f.write(f"# Populate namespace for {module_name}\n")
                        # Add to full namespace path (e.g., qrcode.base.rs_blocks)
                        for export in exports:
                            f.write(f"{module_name}.{export} = {export}\n")

                        f.write("\n")

                    # If this is the main qrcode module, add __all__ aliases immediately
                    if module_name == 'qrcode':
                        all_exports = []
                        for node in ast.walk(stripped_tree):
                            if isinstance(node, ast.Assign):
                                for target in node.targets:
                                    if isinstance(target, ast.Name) and target.id == '__all__':
                                        if isinstance(node.value, ast.List):
                                            for elt in node.value.elts:
                                                if isinstance(elt, ast.Constant):
                                                    all_exports.append(elt.value)

                        if all_exports:
                            f.write("# Add convenience aliases for top-level qrcode module (from __all__)\n")
                            for export in all_exports:
                                # Skip submodule namespaces (they're already set up)
                                submodule_name = f"qrcode.{export}"
                                if submodule_name in created_namespaces:
                                    continue
                                f.write(f"qrcode.{export} = {export}\n")
                            f.write("\n")
                except Exception as e:
                    print(f"Error unparsing {module_name}: {e}")
                    # Fallback: read original file and manually clean imports
                    with open(self.module_paths[module_name], 'r') as orig_f:
                        content = orig_f.read()

                    # Remove import lines while preserving structure
                    lines = content.split('\n')
                    filtered_lines = []
                    in_imports = True

                    for line in lines:
                        stripped = line.strip()

                        # Skip import statements at the beginning
                        if in_imports:
                            if (stripped.startswith('from ') and ' import ' in stripped) or \
                               stripped.startswith('import ') or \
                               not stripped or \
                               stripped.startswith('"""') or \
                               stripped.startswith("'''"):
                                # Skip docstrings and imports at the start
                                if stripped and not stripped.startswith(('import ', 'from ')):
                                    # Non-import, non-empty line found, stop skipping imports
                                    if not stripped.startswith(('"""', "'''")):
                                        in_imports = False
                                        filtered_lines.append(line)
                                continue
                            else:
                                in_imports = False

                        filtered_lines.append(line)

                    # Remove leading empty lines
                    while filtered_lines and not filtered_lines[0].strip():
                        filtered_lines.pop(0)

                    f.write('\n'.join(filtered_lines))
                    f.write("\n\n")

            # Add a single __main__ block at the end
            f.write("# Entry point for CLI usage\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    main()\n")

        print(f"Consolidated file generated: {output_path}")
        print(f"Processed {len(sorted_modules)} modules")


def main():
    if len(sys.argv) != 2:
        print("Usage: python consolidate_qrcode.py <path_to_qrcode_directory>")
        print("Example: python consolidate_qrcode.py ./python-qrcode/qrcode")
        sys.exit(1)

    qrcode_path = sys.argv[1]

    if not os.path.exists(qrcode_path):
        print(f"Error: Path {qrcode_path} does not exist")
        sys.exit(1)

    consolidator = QRCodeConsolidator(qrcode_path)
    consolidator.generate_consolidated_file()


if __name__ == '__main__':
    main()
