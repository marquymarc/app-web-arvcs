#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from scipy.interpolate import interp1d
from textwrap import dedent
app = dash.Dash(
    __name__,
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
    ]
)

df = pd.read_csv('data.csv')
df['cumsum'] = df['co2'].cumsum()


app.layout = html.Div(
    [
        # Top Banner
        html.Div([
            html.H1("Reforestation Project and VCUs"),
            
            html.A(
                [html.Div(
                className="logo",
                children=[
                    html.Img(
                        src="/assets/logo.png"
                    )
                ],
                ),
                ],
                href="https://www.bondy.earth/#content",
                target="_blank"
            ),
            
    ],
        className='banner'),
    
    #Body of the App
    
    html.Div(
        className="row app-body",
        children=[
            #Graphique et crediting period slider
            html.Div(
                className="div1",
                children=[
                    html.Div(
                        className="crediting-period",
                        children=[
                            html.Div(
                                className="lavel-cred",
                                children=[
                                    html.Label("Crediting Period")  
                                ]),
        
                            dcc.Slider(
                                id='Crediting_period',
                                marks={
                                    20: '20 years',
                                    30: '30 years',
                                    },
                                step=1,
                                tooltip= {'always_visible': True},
                                min=20,
                                max=30,
                                value=30,
                                dots=False,
                                vertical = True,
                                updatemode='drag',
                                className="slider",
                    ),
                            ],
                    ),
                    html.Div(
                        className="graph",
                        children=[
                            dcc.Graph(
                                id='our_graph',
                                figure={
                                    'layout':{
                                        'title': 'Reforestation cost and VCUs Revenue',
                                        'xaxis':{'title': 'Years'},
                                        'yaxis':{'title': 'Cost/Revenue'},
                                        'paper_bgcolor': 'rgba(0,0,0,0)',
                                        'plot_bgcolor': 'rgba(0,0,0,0)'
                                        
                                    }
                                }
                            ),
        
                        ],
                    ),
                ],
            
            ),
            
            
            # Turnover Variables
            html.Div(
                className="turnover",
                children=[
                    html.Div(
                        className="label-turnover",
                        children=[
                            html.H4("Turnover Variables", style={'text-align': 'center'})
                        ]
                    ),
                    html.Div(
                        className="label-co2",
                        children=[
                            html.Label('Estimated Annual Volume of CO2 sequestrated')
                        ]
                    
                    ),
                    
                    html.Div(
                        className="slider-tco2",
                        children=[
                            dcc.Slider(
                                id='Estimated_Annual_tCO2',
                                marks={
                                    0: '0',
                                    15000: '15 000',
                                },
                                step=10,
                                tooltip= {'always_visible': True, 'color': 'rgba(0,0,0,0)'},
                                min=0,
                                max=15000,
                                value=7500,
                                dots=False,
                                updatemode='drag')
                        ]
                    
                    ),
                    
                    html.Div(
                        className="label-price",
                        children=[
                            html.Label('Price of Carbon Credits "$/tCO2"')
                        ]
                    
                    ),
                    
                    html.Div(
                        className="slider-price",
                        children=[
                            dcc.Slider(
                            id='Price_tCO2',
                            marks={
                                0: '$0',
                                20: '$20'
                            },
                            step=0.1,
                            tooltip= {'always_visible': True},
                            min=0,
                            max=20,
                            value=10,
                            dots=False,
                            updatemode='drag')
                        ],
                    
                    ),
                                    
                ],                
            
            ),
            
            # Break Even Point
            
            html.Div(
                className="bep",
                children=[
                    html.Div(
                        className="label-bep",
                        children=[
                            html.H4("Break Even Point",
                                    className='text-center',
                                   style={'text-align': 'center'})
                        ]
                    
                    ),     
                    
                    html.Div(
                        className="result-bep",
                        id='intersection',
                        style={'text-align': 'center'}),
                    html.P(
                        'Years',
                        className='years',
                    )
                ],
            ),
            
            #Mean tCO2
            
             html.Div(
                className="mean",
                children=[
                    html.Div(
                        className="label-mean",
                        children=[
                            html.H4("Average Annual ERs",
                                    className='text-left',
                                   style={'text-align': 'left'}),
                            html.Div(
                                className="result-mean",
                                id='result_mean',
                                style={'text-align': 'center'})
                            
                        ]
                    
                    ),  
                ],
             ),
              
            
            # Cost Variables
            
            html.Div(
                className="cost-variables",
                children=[
                    html.Div(
                        className="label-costv",
                        children=[
                            html.H4("Cost Variables", style={'text-align': 'center'})
                        ]                    
                    ),
                    
                    html.Div(
                        className="label-ha",
                        children=[
                            html.Label('Hectares of Land')
                        ]
                    
                    ),
                    
                    html.Div(
                        className="slider-ha",
                        children=[
                            dcc.Slider(
                                id='Hectares_of_land',
                                marks={
                                    0: '0 ha',
                                    300: '300 ha',
                                },
                                step=1,
                                tooltip= {'always_visible': True},
                                min=0,
                                max=300,
                                value=150,
                                dots=False,
                                updatemode='drag')
                        ]
                    
                    ),
                    
                    html.Div(
                        className="label-implementation-cost",
                        children=[
                            html.Label('Implementation Costs (/ha)')
                        ]
                    
                    ),
                    
                    html.Div(
                        className="slider-implementation",
                        children=[
                            dcc.Slider(
                                id='implementation_costs',
                                marks={
                                    0: '$ 0',
                                    15000: '$ 15000',
                                },
                                step=10,
                                tooltip= {'always_visible': True},
                                min=0,
                                max=15000,
                                value=4000,
                                dots=False,
                                updatemode='drag')
                        ]                      
                    ),
                    
                    
                    
                    html.Div(
                        className="label-subsequent-man",
                        children=[
                            html.Label('Subsequent Management Costs(/ha/year)')
                        ]
                    
                    ),
                    
                    html.Div(
                        className="slider-subsequent-man",
                        children=[
                            dcc.Slider(
                                id='subsequent_man',
                                marks={
                                    0: '$ 0',
                                    1000: '$ 1000',
                                },
                                step=5,
                                tooltip= {'always_visible': True},
                                min=0,
                                max=1000,
                                value=200,
                                dots=False,
                                updatemode='drag')
                        ]                      
                    ),
                    
                    html.Div(
                        className="label-gap",
                        children=[
                            html.Label('Gap Analysis Fee')
                        ]
                    ),
                    
                    html.Div(
                        className="slider-gap",
                        children=[
                            dcc.Slider(
                                id='Gap_analysis_fee',
                                marks={
                                    0: '$ 0',
                                    20000: '$ 20 000',
                                },
                                step=100,
                                tooltip= {'always_visible': True},
                                min=0,
                                max=20000,
                                value=0,
                                dots=False,
                                updatemode='drag')
                            ]
                    ),
                    
                    html.Div(
                        className="label-audit",
                        children=[
                            html.Label('Audit Fees')
                        ]
                    ),
                    
                    html.Div(
                        className="slider-audit",
                        children=[
                            dcc.Slider(
                                id='Audit_fee',
                                marks={
                                    10000: '$ 10 000',
                                    30000: '$ 30 000',
                                },
                                step=100,
                                tooltip= {'always_visible': True},
                                min=10000,
                                max=30000,
                                value=25000,
                                dots=False,
                                updatemode='drag'),
                                ]
                    ),
                    
                    html.Div(
                        className="label-consulting",
                        children=[
                            html.Label('Consulting Fees')
                        ]
                    ),
                    
                    html.Div(
                        className="slider-consulting",
                        children=[
                            dcc.Slider(
                                id='consult_fee',
                                marks={
                                    0: '$ 0',
                                    25000: '$ 25 000',
                                },
                                step=100,
                                tooltip= {'always_visible': True},
                                min=0,
                                max=25000,
                                value=15000,
                                dots=False,
                                updatemode='drag'),
                                ]
                    ),
                    
                    
                ],
            ),
            
            #BIP
            
            html.Div(
                className="bip",
                children=[
                    html.Div(
                        className="label-bip",
                        children=[
                            html.H4("ERs needed to Break Even",
                                    style={'text-align': 'center'})
                        ]
                    
                    ),     
                    
                    html.Div(
                        className="result-bip",
                        id='result_bip',
                        style={'text-align': 'center'}),
                    html.P(
                        'Tonnes of Co2',
                        className='Co2')
                ]
            
            ),
            
            #Paragraphe
            
            html.Div(
                        className="par",
                        children=[
                            dcc.Markdown(
                                children=dedent(
                                    """
                                                
                                This app enhances visualization of the costs and revenues associated with a reforestation project which seeks to generate Verified Carbon Units (VCUs).
                                Verra could not certify that the costs formulas are reliable due to their independent status, though, we tried to be as reliable as we could.
                                You can find more about Verra's cost on the [fee schedule](https://verra.org/wp-content/uploads/2020/04/Program-Fee-Schedule_v4.1.pdf)
                                
                                ### How to use the app ?
                                
                                On both mode (linear and Precise), you can adjust the crediting period, the price you estime you can sell VCUs and all every Cost Variables.
                                
                                The "Break Even Point" shows an estimation of which year you can break even with the cost of the project with the sales of VCUs.
            
                                #### Linear Mode
                                
                                The linear mode was made for project manager that don't have precise estimations of how many tonnes of CO2 the reforestation is going to sink, thus, you can 
                                change the "Estimated Annual Volume of CO2 sequestrated" to adjust the "Turnover" line.
                                
                                #### Precise Mode
                                
                                The precise mode was made for project manager that have precise estimations of how many tonnes of CO2 the project is going to sink.
                                
                                You can complete the table on the top-right hand of the app. The Datatable was completed according to one of our project but you can edit it.
                                Once you decrease the crediting and increase it again, all data in the table are deleted, if you do this, you have to complete each rows manually for the app
                                to work.
                                
                                
                                If you have any questions about the app or ways to improve it, let me know at: marc.fonteneau@bondy.earth
                                    """),
                            ),
                        ],
            ),
            
            
            # Dropdown
            
            html.Div(
                className="dropdown",
                children=[
                    dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': 'linear', 'value': 'linear'},
                        {'label': 'precise', 'value': 'precise'}
                    ],
                    value='precise'
                ),
                ],
            ),
            
            # Datatable
            
            html.Div(
                className="table",
                children=[
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name":i, "id":i} for i in df.columns],
                        data=df.to_dict('records'),
                        editable=True,
                        style_table={'height': '523.4px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center',
                                   'backgroundColor': '#E7F7DA',
                                    'color': 'black',
                                    'font-family': 'sans-serif'
                                   },
                        style_header={
                            'backgroundColor': '#26331B',
                            'color': 'white',
                            'font-size': '14px'
                        }
    
                    ),
                    
                ],               
            
            ),   
            
        ],
    ),
    ],
)
    
    
@app.callback(
    Output('table', 'data'),
    Input('Crediting_period', 'value'),
    State('table', 'data'),
)
def update_data_table(rows, records):
    columns=[{"name":i, "id":i, "type": "numeric"} for i in df.columns]
    change = rows - len(records)
    if change > 0:
        for i in range(change):
            records.append({c["id"]: "" for c in columns})
    elif change < 0:
        records = records[:rows]
        
    return records

@app.callback(
    [Output(component_id='our_graph', component_property='figure'),
    Output(component_id='intersection', component_property='children'),
    Output(component_id='result_mean', component_property='children'),
    Output(component_id='result_bip', component_property='children')],
    [Input(component_id='Estimated_Annual_tCO2', component_property='value'),
    Input(component_id='Price_tCO2', component_property='value'),
    Input(component_id='Hectares_of_land', component_property='value'),
    Input(component_id='implementation_costs', component_property='value'),
    Input(component_id='subsequent_man', component_property='value'), 
    Input(component_id='Gap_analysis_fee', component_property='value'),
    Input(component_id='Audit_fee', component_property='value'),
    Input(component_id='Crediting_period', component_property='value'),
    Input(component_id='table', component_property='data'),
    Input(component_id='dropdown', component_property='value'),
    Input(component_id='consult_fee', component_property='value')]  
)
    
def update_graph(Est_ann_emissions, Price, Hectares_of_land, implementation_costs, subsequent_man, Gap_fee, Audit_fee, Cred_period, rows, dropdown, consult_fee):
    m= Cred_period
    x=np.arange(0, m)
    a= implementation_costs*Hectares_of_land + subsequent_man*x*Hectares_of_land
    c= 500 + 0.1*Est_ann_emissions + 0.05*Est_ann_emissions + 375 + 2500*x + Gap_fee + consult_fee
    b= a + c
    dff = pd.DataFrame(rows).astype(int)
   
    
    if dropdown=='linear':
        y=x*Est_ann_emissions*Price
        fig = go.Figure()
        fig.layout.xaxis.title='Years'
        fig.layout.yaxis.title='Cost & Revenue ($)'
        fig.layout.paper_bgcolor='rgba(0,0,0,0)'
        fig.layout.plot_bgcolor='#E7F7DA'
        fig.add_trace(go.Scatter(x=x, y=y, name='Turnover', line=dict(color='#037F8C')))
        fig.add_trace(go.Scatter(x=x, y=a, name='Operating Costs', line = dict(color='#F27507', dash='dash')))
        fig.add_trace(go.Scatter(x=x, y=c, name='Certification Costs', line=dict(color='#F2B90C', dash='dash')))
        fig.add_trace(go.Scatter(x=x, y=b, name='Total costs', line=dict(color='#590202')))   
        bep = interp1d(y - b, x, fill_value="extrapolate")(0)
        bep = bep.round(2)
       
    else :
        y = dff['cumsum']*Price
        fig = px.line(dff, x='year', y=y)
        fig.add_trace(go.Scatter(x=x, y=a, name='Operating Costs', line = dict(color='#F27507', dash='dash')))
        fig.add_trace(go.Scatter(x=x, y=c, name='Certification Costs', line=dict(color='#F2B90C', dash='dash')))
        fig.add_trace(go.Scatter(x=x, y=b, name='Total costs', line=dict(color='#590202')))
        fig.layout.xaxis.title='Years'
        fig.layout.yaxis.title='Cost & Revenue ($)'
        fig.layout.paper_bgcolor='rgba(0,0,0,0)'
        fig.layout.plot_bgcolor='#E7F7DA'
        y = fig.data[0].y
        y = np.array(y)
        y = (np.array(list(map(int, y))))
        bep = interp1d(y - b, x, fill_value="extrapolate")(0)
        bep = bep+1.11
        bep = bep.round(2)
    
    
    if dropdown=='linear':
        i = Est_ann_emissions
        e = i
        
    else:
        i=dff['co2']
        e = np.mean(i)
        e = round(e, 2)
    
    if dropdown=='linear':
        bip = bep * Est_ann_emissions
        bip = round(bip, 2)
        
    else:
        bip = e*bep
        bip=round(bip, 2)


    return fig, bep, e, bip

if __name__ == '__main__':
    app.run_server(debug=False)

