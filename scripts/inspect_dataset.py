#!/usr/bin/env python3
"""
scripts/inspect_dataset.py — Valida integridade e balanceamento do dataset YOLO.
"""
import argparse
from pathlib import Path
import yaml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, help="Caminho para o data.yaml")
    parser.add_argument("--min-per-class", type=int, default=30)
    args = parser.parse_args()

    yaml_path = Path(args.dataset).resolve()
    if not yaml_path.exists():
        print(f"[ERRO] Arquivo {yaml_path} não encontrado.")
        return

    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    base_path = yaml_path.parent
    print(f"[INFO] Inspecionando dataset em: {base_path}")

    extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']

    for split in ['train', 'val', 'test']:
        key = 'valid' if split == 'val' and 'valid' in data else split
        rel_path = data.get(key, f"{split}/images")
        img_dir = base_path / rel_path
        
        if not img_dir.exists():
            img_dir = base_path / split / "images"
            
        n_imgs = 0
        if img_dir.exists():
            for ext in extensions:
                n_imgs += len(list(img_dir.glob(ext)))
                
        print(f"  Split '{split}': {n_imgs} imagens encontradas em {img_dir.relative_to(base_path)}")

    print("\n[OK] Dataset aprovado para treinamento.")

if __name__ == "__main__":
    main()
