function generate_network(sp_node, sp_edges) {
    var cy = cytoscape({
        container: document.getElementById('cy'),

        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(name)',
                    'text-valign': 'center',
                    'color':"white",
                    'text-outline-color': 'data(color)',
                    'text-outline-width': 2,
                    'shape':'data(shape)',
                    'background-color': 'data(color)',
                }
            },

            {
                selector: 'edge',
                style: {
                    'width':2,
                    'line-color':'grey',
                }
            },

            {
                    selector: 'node.highlight',
                        style: {
                            'label': 'data(name)',
                            'text-valign': 'center',
                            'color':"white",
                            'text-outline-color': 'black',
                            'text-outline-width': 2,
                            'background-color': 'black',
                        }
                },


            ],

        elements: {

            nodes: sp_node,
            edges: sp_edges
        },

      layout: {
        name: 'cose',
        idealEdgeLength: 100,
        nodeOverlap: 20,
        refresh: 20,
        fit: true,
        padding: 30,
        randomize: false,
        componentSpacing: 100,
        nodeRepulsion: 400000,
        edgeElasticity: 100,
        nestingFactor: 5,
        gravity: 80,
        numIter: 1000,
        initialTemp: 200,
        coolingFactor: 0.95,
        minTemp: 1.0,
      },
        pan:{x:15,y:15},
        zoom:0.6,
        minZoom:0.5,
        maxZoom:3,
        motionBlur: true,
        wheelSensitivity: 0.05,
    });

    cy.on('tap', 'node', function(e){
        var ele = e.target;
        cy.elements().difference(ele.outgoers());
        ele.addClass('highlight').outgoers().addClass('highlight');
    });

    cy.on('cxttap', 'node', function(e){
        var ele = e.target;
        ele.removeClass('highlight').outgoers().removeClass('highlight');
    });


};

