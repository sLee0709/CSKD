    var all_edges = new Array()
    var all_nodes = new Array()
    for(let i = 0; i<edge_array.length;i++){
        var edge_datas = {data: {id:edge_array[i][0]+"_"+edge_array[i][1], source:edge_array[i][0], target: edge_array[i][1]}}
        all_edges.push(edge_datas)
    };

    for (let n = 0; n<source_gene_array.length; n++){
        var source_node_datas = {data: {id:source_gene_array[n], name:source_gene_array[n], color:'orange', shape:'pentagon'}}
        all_nodes.push(source_node_datas)
    };

    for (let j = 0; j<gene_array.length; j++){
        var node_datas = {data: {id:gene_array[j], name:gene_array[j], color:'#191970', shape:'ellipse'}}
        all_nodes.push(node_datas)
    };


    var network_style = 'cose';

    // globalize cy
    var cy = cytoscape({
        container: document.getElementById('cy'),

        style: [
            {

                selector: 'node',
                style: {
                    'label': 'data(name)',
                    'text-valign': 'center',
                    'color':"white",
                    'text-outline-color': '#191970',
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
                        'text-outline-color': '#FA8072',
                        'text-outline-width': 2,
                        'background-color': '#FA8072',
                    }
            },

            {
                selector: 'edge.highlight',
                    style: {
                    'width':3,
                    'line-color':'#FA8072',
                    }
            },


            {
                selector: 'edge.highlight',
                    style: {
                    'width':3,
                    'line-color':'#FA8072',
                    }
            },

            {
                selector: 'node.main_highlight',
                    style: {
                        'label': 'data(name)',
                        'text-valign': 'center',
                        'color':"white",
                        'text-outline-color': '#00CED1',
                        'text-outline-width': 2,
                        'background-color': '#00CED1',
                    }
            },

            {
                selector: 'node[background_color]',
                style: {
                    'background-color': 'data(background_color)',
                    'text-outline-color': 'data(background_color)',
                }
            },

            {
                selector: 'node.semitransp',
                style:{ 'opacity': '0.5' }
            },

            ],

        elements: {

            nodes: all_nodes,
            edges: all_edges,
        },

      layout: {
            name: network_style,
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
            minTemp: 1.0
          },
            motionBlur: true,
            wheelSensitivity: 0.05,

        });


    //cytoscape network initializaiton

    function cytoNet(){

    cy.on('tap', 'node', function(e){
        var ele = e.target;
        if(cy.elements('node[background-color:orange]')){
            cy.elements().difference(ele.outgoers());
            ele.addClass('main_highlight').outgoers().addClass('highlight');
        }
    });

    cy.on('cxttap', 'node', function(e){
        var ele = e.target;
        ele.removeClass('main_highlight').outgoers().removeClass('highlight');
    });

    };


    $('#inquiry_specific_gene_button').on('click', function () {
        var datas = $('#specific_genes').val()
        var gene_array = new Array(datas)
        var csrf = $('#tar_name').data('csrf')

        $.ajax({
            type:'GET',
            url:'./',
            traditional:true,
            data:{
                action:'specific_genes_highlights',
                async:false,
                specific_gene_list:gene_array,
                csrfmiddlewaretoken:csrf
            },
            beforeSend:function () {
                $('#graph_status').html("Sending...")
                $('.ui.active.dimmer').show()
            },
            success:function (response) {
                $('.ui.active.dimmer').hide()
                $('#graph_status').html("Success!")
                var t = $.parseJSON(response)
                if (t.code == 2){
                    all_eles = cy.elements();
                    all_eles.removeClass('main_highlight').outgoers().removeClass('highlight');
                for (let m = 0; m<t.sg.length; m++){
                    var eles = cy.filter('node[name = "'+t.sg[m]+'"]')
                    cy.elements().difference(eles.outgoers());
                    eles.addClass('main_highlight').outgoers().addClass('highlight');
                };


                cy.on('tap', 'node', function(e){
                    var ele = e.target;
                    if(cy.elements('node[background-color:orange]')){
                        cy.elements().difference(ele.outgoers());
                        ele.addClass('main_highlight').outgoers().addClass('highlight');
                    }
                });


                cy.on('cxttap', '*/', function(e){
                    var ele = e.target;
                    ele.removeClass('main_highlight').outgoers().removeClass('highlight');
                });

                }
                else {
                    $('#graph_status').html('error')
                }
            }
        })
    })

    $('.ui.small.item').on('click', function () {
        var new_name = $(this).text()
        var csrf = $('#tar_name').data('csrf')
        var datas = $('#specific_genes').val()
        var gene_array = new Array(datas)
        console.log(gene_array)
        $.ajax({
            type:'GET',
            url:'./',
            traditional:true,
            data:{
                action:'change_style',
                async:false,
                new_style:new_name,
                specific_gene_list:gene_array,
                csrfmiddlewaretoken:csrf
            },
            beforeSend:function () {
                $('#graph_status').html("Sending...")
                $('.ui.active.dimmer').show()
            },
            success:function (response) {
                $('.ui.active.dimmer').hide()
                $('#graph_status').html("Success!")
                var t = $.parseJSON(response)
                if (t.code == 1){
                    network_style = t.style
                    var cy = cytoscape({
                        container: document.getElementById('cy'),

                        style: [
                            {
                                selector: 'node',
                                style: {
                                    'label': 'data(name)',
                                    'text-valign': 'center',
                                    'color':"white",
                                    'text-outline-color': '#191970',
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
                                        'text-outline-color': '#FA8072',
                                        'text-outline-width': 2,
                                        'background-color': '#FA8072',
                                    }
                            },

                            {
                                selector: 'edge.highlight',
                                    style: {
                                    'width':3,
                                    'line-color':'#FA8072',
                                    }
                            },

                            {
                                selector: 'node.main_highlight',
                                    style: {
                                        'label': 'data(name)',
                                        'text-valign': 'center',
                                        'color':"white",
                                        'text-outline-color': '#00CED1',
                                        'text-outline-width': 2,
                                        'background-color': '#00CED1',
                                    }
                            },

                            {
                                selector: 'node[background_color]',
                                style: {
                                    'background-color': 'data(background_color)',
                                    'text-outline-color': 'data(background_color)',
                                }
                            },

                            {
                                selector: 'node.semitransp',
                                style:{ 'opacity': '0.5' }
                            },

                            ],

                        elements: {

                            nodes: all_nodes,
                            edges: all_edges,
                        },

                      layout: {
                        name: network_style,
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
                        minTemp: 1.0
                      },
                        motionBlur: true,
                        wheelSensitivity: 0.05,

                    });
                    for (let m = 0; m<t.sg.length; m++){
                    var eles = cy.filter('node[name = "'+t.sg[m]+'"]')
                        cy.elements().difference(eles.outgoers());
                        eles.addClass('main_highlight').outgoers().addClass('highlight');
                    };
                    cytoNet()



                    cy.on('tap', 'node', function(e){
                        var ele = e.target;
                        if(cy.elements('node[background-color:orange]')){
                            cy.elements().difference(ele.outgoers());
                            ele.addClass('main_highlight').outgoers().addClass('highlight');
                        }
                    });


                    cy.on('cxttap', '*/', function(e){
                        var ele = e.target;
                        ele.removeClass('main_highlight').outgoers().removeClass('highlight');
                    });

                    $('#inquiry_specific_gene_button').on('click', function () {
                        var datas = $('#specific_genes').val()
                        var gene_array = new Array(datas)
                        var csrf = $('#tar_name').data('csrf')

                        $.ajax({
                            type:'GET',
                            url:'./',
                            traditional:true,
                            data:{
                                action:'specific_genes_highlights',
                                async:false,
                                specific_gene_list:gene_array,
                                csrfmiddlewaretoken:csrf
                            },
                            beforeSend:function () {
                                $('#graph_status').html("Sending...")
                                $('.ui.active.dimmer').show()
                            },
                            success:function (response) {
                                $('.ui.active.dimmer').hide()
                                $('#graph_status').html("Success!")
                                var t = $.parseJSON(response)
                                if (t.code == 2){
                                    all_eles = cy.elements();
                                    all_eles.removeClass('main_highlight').outgoers().removeClass('highlight');
                                    for (let m = 0; m<t.sg.length; m++){
                                        var eles = cy.filter('node[name = "'+t.sg[m]+'"]')
                                            cy.elements().difference(eles.outgoers());
                                            eles.addClass('main_highlight').outgoers().addClass('highlight');
                                    };

                                    cy.on('tap', 'node', function(e){
                                        var ele = e.target;
                                        if(cy.elements('node[background-color:orange]')){
                                            cy.elements().difference(ele.outgoers());
                                            ele.addClass('main_highlight').outgoers().addClass('highlight');
                                        }
                                    });


                                    cy.on('cxttap', '*/', function(e){
                                        var ele = e.target;
                                        ele.removeClass('main_highlight').outgoers().removeClass('highlight');
                                    });

                                }
                                else {
                                    $('#graph_status').html('error')
                                }
                            }
                        })
                    })

                    save_img = function() {
                        var png64 = cy.png();
                        $('#ex_png').attr('src', png64)
                    };
                }
                else {
                    $('#graph_status').html('error')
                }
            }
        })
    })




    save_img = function() {
        var png64 = cy.png('')
        $('#ex_png').attr('src', png64)
    };



