"""
Image Enhancement Deployment Module
Deploys Flask app using pyngrok for public URL access
"""

from flask import Flask
import sys
import os
from pyngrok import ngrok
from pyngrok import conf

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from interfaces.flask_app import app


def deploy_with_ngrok(port=5000, auth_token=None):
    """
    Deploy Flask app using ngrok tunnel
    
    Args:
        port (int): Port to run Flask on
        auth_token (str): Ngrok authentication token (optional)
        
    Returns:
        str: Public URL provided by ngrok
    """
    
    # Set auth token if provided
    if auth_token:
        ngrok.set_auth_token(auth_token)
    
    try:
        print("\n" + "="*60)
        print("🚀 Starting Image Enhancement App Deployment")
        print("="*60)
        
        # Create ngrok tunnel
        print(f"\n📡 Creating ngrok tunnel on port {port}...")
        public_url = ngrok.connect(port)
        
        print(f"✅ Tunnel created!")
        print(f"\n🌐 Public URL: {public_url}")
        print(f"📍 Local URL: http://localhost:{port}")
        
        print("\n" + "-"*60)
        print("API Documentation available at:")
        print(f"  {public_url}/")
        print("-"*60 + "\n")
        
        # Start Flask app
        print("🔄 Starting Flask server...")
        app.run(port=port, debug=False)
        
        return public_url
        
    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        raise
    finally:
        # Cleanup
        ngrok.kill()


def run_streamlit():
    """Launch Streamlit interface"""
    import subprocess
    
    streamlit_path = os.path.join(os.path.dirname(__file__), 
                                 'src', 'interfaces', 'streamlit_app.py')
    
    print("\n" + "="*60)
    print("🎨 Starting Streamlit Interface")
    print("="*60)
    
    try:
        subprocess.run(['streamlit', 'run', streamlit_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
    except FileNotFoundError:
        print("StreamLit not found. Install with: pip install streamlit")


def run_flask():
    """Run Flask API without ngrok"""
    print("\n" + "="*60)
    print("🖥️  Running Flask API")
    print("="*60)
    print("\n📍 API available at: http://localhost:5000")
    print("-"*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Image Enhancement Application Launcher'
    )
    parser.add_argument(
        'interface',
        choices=['flask', 'streamlit', 'ngrok'],
        help='Interface to launch'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to run on (default: 5000)'
    )
    parser.add_argument(
        '--auth-token',
        help='Ngrok authentication token'
    )
    
    args = parser.parse_args()
    
    if args.interface == 'flask':
        run_flask()
    
    elif args.interface == 'streamlit':
        run_streamlit()
    
    elif args.interface == 'ngrok':
        deploy_with_ngrok(port=args.port, auth_token=args.auth_token)


if __name__ == '__main__':
    # Default: run Flask
    # For other interfaces, run: python deploy.py [streamlit|ngrok]
    main()
