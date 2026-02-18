"""
Setup utility to register existing KML files in the database
"""
import os
import shutil
from pathlib import Path
from app import create_app, db
from app.models import KMLGeneration

def register_existing_kml():
    """Register existing KML files from KML_Output directory"""
    app = create_app('development')
    
    with app.app_context():
        # Path to KML_Output directory (parent directory)
        repo_path = Path(os.getenv('KML_REPO_PATH', '../'))
        kml_output_dir = repo_path / 'KML_Output'
        downloads_dir = Path('app/static/downloads')
        
        if not kml_output_dir.exists():
            print(f"KML_Output directory not found at {kml_output_dir}")
            return
        
        # Find all KML files
        kml_files = list(kml_output_dir.glob('*.kml'))
        
        if not kml_files:
            print("No KML files found in KML_Output directory")
            return
        
        for kml_file in sorted(kml_files, key=lambda f: f.stat().st_mtime, reverse=True):
            # Check if already registered
            existing = KMLGeneration.query.filter_by(filename=kml_file.name).first()
            if existing:
                print(f"KML file already registered: {kml_file.name}")
                continue
            
            # Copy to static/downloads
            downloads_dir.mkdir(parents=True, exist_ok=True)
            dest_path = downloads_dir / kml_file.name
            
            try:
                shutil.copy2(kml_file, dest_path)
                print(f"Copied {kml_file.name} to static/downloads/")
            except Exception as e:
                print(f"Failed to copy {kml_file.name}: {str(e)}")
                continue
            
            # Calculate file stats
            file_size_mb = kml_file.stat().st_size / (1024 * 1024)
            
            # Register in database
            kml_gen = KMLGeneration(
                filename=kml_file.name,
                filepath=str(kml_file),
                file_size_mb=file_size_mb,
                status='success'
            )
            
            db.session.add(kml_gen)
            db.session.commit()
            
            print(f"Registered KML file: {kml_file.name} ({file_size_mb:.2f} MB)")
        
        print("KML file registration complete!")

if __name__ == '__main__':
    register_existing_kml()
