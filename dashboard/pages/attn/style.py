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
        "selector": "node:selected",
        "style": {
            "background-color": "#5e2390",
            "background-opacity": ".7",
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
