#!/usr/bin/env python3
"""
Image Optimization Script for juei.co.in Portfolio
Compresses JPEG images to reduce file size by 50-60%
"""

import os
import sys
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow -q")
    from PIL import Image

def optimize_image(input_path, quality=85, max_width=2000):
    """
    Optimize a single image by compressing and resizing
    """
    try:
        img = Image.open(input_path)
        original_size = os.path.getsize(input_path)
        
        # Convert RGBA to RGB if necessary (for JPEGs)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Resize if too large (max width 2000px)
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save with optimization
        img.save(input_path, 'JPEG', quality=quality, optimize=True)
        
        new_size = os.path.getsize(input_path)
        reduction = ((original_size - new_size) / original_size) * 100
        
        return {
            'file': os.path.basename(input_path),
            'original_kb': round(original_size / 1024, 2),
            'optimized_kb': round(new_size / 1024, 2),
            'reduction_percent': round(reduction, 2),
            'status': '✅ OPTIMIZED'
        }
    except Exception as e:
        return {
            'file': os.path.basename(input_path),
            'status': f'❌ ERROR: {str(e)}'
        }

def main():
    portfolio_path = Path("assets/img/portfolio")
    
    if not portfolio_path.exists():
        print("❌ Portfolio directory not found!")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🖼️  IMAGE OPTIMIZATION REPORT")
    print("="*70 + "\n")
    
    results = []
    total_original = 0
    total_optimized = 0
    
    # Process all images in portfolio subdirectories
    for image_file in portfolio_path.rglob('*.jpg'):
        result = optimize_image(str(image_file), quality=85)
        results.append(result)
        
        if 'original_kb' in result:
            total_original += result['original_kb']
            total_optimized += result['optimized_kb']
            print(f"✅ {result['file']}")
            print(f"   Before: {result['original_kb']} KB | After: {result['optimized_kb']} KB | Reduction: {result['reduction_percent']}%\n")
    
    # Process JPEG files
    for image_file in portfolio_path.rglob('*.jpeg'):
        result = optimize_image(str(image_file), quality=85)
        results.append(result)
        
        if 'original_kb' in result:
            total_original += result['original_kb']
            total_optimized += result['optimized_kb']
            print(f"✅ {result['file']}")
            print(f"   Before: {result['original_kb']} KB | After: {result['optimized_kb']} KB | Reduction: {result['reduction_percent']}%\n")
    
    # Print summary
    print("\n" + "="*70)
    print("📊 OPTIMIZATION SUMMARY")
    print("="*70)
    print(f"Total Images Processed: {len([r for r in results if 'original_kb' in r])}")
    print(f"Total Original Size: {round(total_original / 1024, 2)} MB")
    print(f"Total Optimized Size: {round(total_optimized / 1024, 2)} MB")
    print(f"Total Reduction: {round(((total_original - total_optimized) / total_original) * 100, 2)}%")
    print(f"Total Size Saved: {round((total_original - total_optimized) / 1024, 2)} MB")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    main()
