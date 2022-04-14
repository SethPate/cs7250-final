stylesheet = [
    # Group selectors
    {
        "selector": "core",
        "style": {
            "active-bg-size": 0,
        },
    },
    {
        "selector": "node",
        "style": {
            "content": "data(label)",
            "text-halign": "center",
            "text-valign": "center",
            "width": "100px",
            "height": "14px",
            "shape": "square",
            "overlay-opacity": 0,
        },
    },
    {
        "selector": ".node-word",
        "style": {
            "color": "black",
            "background-color": "white",
            "padding": "3px",
            "border-color": "black",
            "border-width": "2px",
            "font-size": "16px",
        },
    },
    {
        "selector": ".edge-attention",
        "style": {
            "width": "data(weight)",
            "lineColor": "black",
            # "target-arrow-shape": "vee",
            "curve-style": "bezier",
            'source-endpoint': '50% 0',
            'target-endpoint': '-50% 0'
            # "arrow-scale": "data(weight)*5",
        },
    },
    {
        "selector": ".node-header",
        "style": {
            "background-color": "white",
            "border-width": "0px",
            "font-size": "20px",
            "fontWeight": "bold",
        },
    },
    {
        "selector": "node:selected",
        "style": {
            "background-color": "yellow",
        },
    },
    {
        "selector": ".node-output",
        "style": {
            "background-color": "data(color)",
            "border-width": "1px",
            "width": "10px",
            "height": "9px",
        },
    },
    {
        "selector": ".node-class",
        "style": {
            "background-color": "data(color)",
            "border-width": "3px",
            "width": "100px",
            "height": "100px",
        },
    },
]
