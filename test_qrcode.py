#!/usr/bin/env python3
"""
Test qrcode.py against golden masters.

Copyright (c) 2025 c4ffein
Licensed under the MIT License - see LICENSE file for details
"""
import subprocess
import sys
from pathlib import Path
import tempfile

# Import the consolidated qrcode module
import qrcode

def generate_qr_text_lib(data):
    """Generate QR code as text output using the library."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Get text representation
    lines = []
    for row in qr.modules:
        line = ''.join('██' if cell else '  ' for cell in row)
        lines.append(line)
    return '\n'.join(lines)

def generate_qr_text_cli(data):
    """Generate QR code as text output using the CLI."""
    # Use --ascii flag to force ASCII output even when piped
    result = subprocess.run(
        ['python', 'qrcode.py', '--ascii'],
        input=data,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"CLI failed: {result.stderr}")
    return result.stdout.strip()

def create_golden_masters():
    """Create golden master test files."""
    test_cases = {
        'small': 'small',
        'medium': 'This is a medium length test string for QR code generation',
        'large': 'This is a much longer test string that will generate a large QR code with more data capacity and complexity to properly test the QR code generation'
    }

    golden_dir = Path('golden_masters')
    golden_dir.mkdir(exist_ok=True)

    for name, data in test_cases.items():
        # Create library golden master
        output_lib = generate_qr_text_lib(data)
        golden_path_lib = golden_dir / f'{name}_lib.txt'
        golden_path_lib.write_text(output_lib)
        print(f'Created {golden_path_lib}')

        # Create CLI golden master
        output_cli = generate_qr_text_cli(data)
        golden_path_cli = golden_dir / f'{name}_cli.txt'
        golden_path_cli.write_text(output_cli)
        print(f'Created {golden_path_cli}')

def test_golden_masters():
    """Test against golden masters."""
    test_cases = {
        'small': 'small',
        'medium': 'This is a medium length test string for QR code generation',
        'large': 'This is a much longer test string that will generate a large QR code with more data capacity and complexity to properly test the QR code generation'
    }

    golden_dir = Path('golden_masters')
    all_passed = True

    for name, data in test_cases.items():
        # Test library usage
        golden_path_lib = golden_dir / f'{name}_lib.txt'
        if not golden_path_lib.exists():
            print(f'❌ {name} (lib): Golden master not found')
            all_passed = False
        else:
            expected_lib = golden_path_lib.read_text()
            actual_lib = generate_qr_text_lib(data)
            if expected_lib == actual_lib:
                print(f'✅ {name} (lib): PASS')
            else:
                print(f'❌ {name} (lib): FAIL')
                all_passed = False

        # Test CLI usage
        golden_path_cli = golden_dir / f'{name}_cli.txt'
        if not golden_path_cli.exists():
            print(f'❌ {name} (cli): Golden master not found')
            all_passed = False
        else:
            try:
                expected_cli = golden_path_cli.read_text()
                actual_cli = generate_qr_text_cli(data)
                if expected_cli == actual_cli:
                    print(f'✅ {name} (cli): PASS')
                else:
                    print(f'❌ {name} (cli): FAIL')
                    all_passed = False
            except Exception as e:
                print(f'❌ {name} (cli): ERROR - {e}')
                all_passed = False

    return all_passed

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'create':
        create_golden_masters()
    else:
        success = test_golden_masters()
        sys.exit(0 if success else 1)
