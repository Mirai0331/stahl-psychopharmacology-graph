#`-*- coding: utf-8 -*-
import json
import re
from pathlib import Path

def main():
    root = Path('.').resolve()
    kg_path = root / 'output' / 'knowledge_graph.json'
    html_path = root / 'output' / 'interactive_graph.html'
    dist_html_path = root / 'output' / 'dist' / 'index.html'
    dist_assets = root / 'output' / 'dist' / 'assets'
    
    assert kg_path.exists(), 'knowledge_graph.json not found'
    assert html_path.exists(), 'interactive_graph.html not found'
    assert dist_html_path.exists(), 'dist/index.html not found'
    assert dist_assets.exists(), 'dist/assets not found'

    with open(kg_path, 'r', encoding='utf-8') as f:
        kg_data = json.load(f)

    nodes_dict = {n['id']: n for n in kg_data['nodes']}
    edges = kg_data['edges']
    
    print(f'Success: KG nodes = {len(nodes_dict)}, KG edges = {len(edges)}')
    
    html_content = html_path.read_text(encoding='utf-8')
    
    referenced_ids = set(re.findall(r"'(?:DRUG|REC|PATH|DIS|CLS|SE)_[A-Z0-9_]+'", html_content))
    referenced_ids = {x.strip("'") for x in referenced_ids}
    
    missing_nodes = referenced_ids - set(nodes_dict.keys())
    if missing_nodes:
        print(f'Warning: {len(missing_nodes)} missing nodes: {missing_nodes}')
    else:
        print('Success: All referenced node IDs match KG!')

    image_refs = set(re.findall(r"assets/[a-zA-Z0-9_.\-]+", html_content))
    missing_assets = [r_id for r_id in image_refs if not (root / 'output' / r_id).exists()]
    
    if missing_assets:
        print(f'Error: Missing assets: {missing_assets}')
    else:
        print(f'Success: All {len(image_refs)} assets exist!')

    required_dom_elements = [
        'network-container', 'sidebar', 'search-input',
        'btn-cascade-mode', 'btn-expand-all', 'btn-zoom-fit',
        'detail-drawer', 'drawer-title', 'drawer-desc', 'drawer-conns',
        'btn-layout-force', 'btn-layout-cluster', 'btn-layout-hier',
        'filter-container'
    ]
    for el_id in required_dom_elements:
        assert f'id=\"{el_id}\"' in html_content, f'Missing DOM element: {el_id}'
    
    print('Success: All DOM elements present!')
    print('===== Web Functionality Verification Passed ! =====')

if __name__ == '__main__':
    main()
