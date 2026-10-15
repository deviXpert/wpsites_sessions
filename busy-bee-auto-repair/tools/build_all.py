"""Rebuild every Busy Bee document + push custom code (run after any change)."""
import subprocess, sys
for s in ('kit.py', 'menus.py', 'build_header.py', 'build_footer.py', 'build_popups.py', 'build_home.py', 'build_services.py', 'code.py'):
    print('>>', s); subprocess.run([sys.executable, s], check=True)
