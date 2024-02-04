import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly as pt

st.set_page_config(layout="wide")

@st.cache_data
def get_0psi():
    spec = pd.read_csv('data/spectrum-0psi.csv')
    peaks = pd.read_csv('data/peaks-0psi.csv')
    pred = pd.read_csv('data/pred-0psiar.csv')
    model = pd.read_csv('data/model-0psiar.csv')
    
    return {'spec':spec,'peaks':peaks,'pred':pred,'model':model}

@st.cache_data
def get_40psi():
    spec = pd.read_csv('data/spectrum-40psi.csv')
    peaks = pd.read_csv('data/peaks-40psiar.csv')
    pred = pd.read_csv('data/pred-40psiar.csv')
    model = pd.read_csv('data/model-40psiar.csv')
    
    return {'spec':spec,'peaks':peaks,'pred':pred,'model':model}

@st.cache_data
def get_ne():
    out = {}
    out['spec'] = pd.read_csv('data/spectrum-ne.csv')
    out['peaks'] = pd.read_csv('data/peaks-ne.csv')
    pred = pd.read_csv('data/pred-isos.csv')
    out['model-isos'] = pd.read_csv(f'data/model-isos.csv')
    out['pred']=pred
    return out

data_0psi = get_0psi()
data_40psi = get_40psi()
data_ne = get_ne()

fig1=go.Figure(go.Scatter(x=data_0psi['spec'].freq, y=data_0psi['spec'].int,mode='lines',name='Experiment',hoverinfo='skip'))
fig1.add_trace(go.Scatter(x=data_0psi['model'].freq, y=data_0psi['model'].int,mode='lines',name='Simulation',hoverinfo='skip'))
fig1.add_trace(go.Scatter(x=data_0psi['peaks']['$x_0$'],y=data_0psi['peaks']['A'],name='Peaks',mode='markers',hovertemplate='%{x:.4f} MHz<br />A: %{y:.3f}',legendgroup='peaks'))
fig1.add_trace(go.Bar(x=data_0psi['peaks']['$x_0$'],y=data_0psi['peaks']['A'],width=0.005,showlegend=False,hoverinfo='skip',legendgroup='peaks'))
fig1.add_trace(go.Scatter(x=data_0psi['pred'].freq,y=-data_0psi['pred'].int,name='Transitions',mode='markers',
                         customdata=data_0psi['pred']['label'].to_numpy(),hovertemplate='%{customdata}',legendgroup='pred'))
fig1.add_trace(go.Bar(x=data_0psi['pred'].freq,y=-data_0psi['pred'].int,width=0.005,showlegend=False,hoverinfo='skip',legendgroup='pred'))
fig1.update_layout(
    xaxis_title="Frequency (MHz)",
    yaxis_title="Intensity (AU)",
)
fig1.update_xaxes(tickformat='digit')


fig2=go.Figure(go.Scatter(x=data_40psi['spec'].freq, y=data_40psi['spec'].int,mode='lines',name='Experiment',hoverinfo='skip'))
fig2.add_trace(go.Scatter(x=data_40psi['model'].freq, y=data_40psi['model'].int,mode='lines',name='Simulation',hoverinfo='skip'))
fig2.add_trace(go.Scatter(x=data_40psi['peaks']['$x_0$'],y=data_40psi['peaks']['A'],name='Peaks',mode='markers',hovertemplate='%{x:.4f} MHz<br />A: %{y:.3f}',legendgroup='peaks'))
fig2.add_trace(go.Bar(x=data_40psi['peaks']['$x_0$'],y=data_40psi['peaks']['A'],width=0.005,showlegend=False,hoverinfo='skip',legendgroup='peaks'))
fig2.add_trace(go.Scatter(x=data_40psi['pred'].freq,y=-data_40psi['pred'].int,name='Transitions',mode='markers',
                         customdata=data_40psi['pred']['label'].to_numpy(),hovertemplate='%{customdata}',legendgroup='pred'))
fig2.add_trace(go.Bar(x=data_40psi['pred'].freq,y=-data_40psi['pred'].int,width=0.005,showlegend=False,hoverinfo='skip',legendgroup='pred'))
fig2.update_layout(
    xaxis_title="Frequency (MHz)",
    yaxis_title="Intensity (AU)",
)
fig2.update_xaxes(tickformat='digit')

color_dict = {
    '13c0': "red",
    '13c2': "yellow",
    '13c3': "lime",
    '13c4': "gray",
    '18o': "white"
}

color = data_ne['pred']['species'].map(color_dict)

fig3=go.Figure(go.Scatter(x=data_ne['spec'].freq, y=data_ne['spec'].int,mode='lines',name='Experiment',hoverinfo='skip'))
for i in ['13c0','13c2','13c3','13c4','18o']:
    fig3.add_trace(go.Scatter(x=data_ne[f'model-isos'].freq, y=data_ne[f'model-isos'][i],mode='lines',name=f'Simulation-{i}',hoverinfo='skip'))
fig3.add_trace(go.Scatter(x=data_ne['peaks']['$x_0$'],y=data_ne['peaks']['A'],name='Peaks',mode='markers',hovertemplate='%{x:.4f} MHz<br />A: %{y:.3f}',legendgroup='peaks'))
fig3.add_trace(go.Bar(x=data_ne['peaks']['$x_0$'],y=data_ne['peaks']['A'],width=0.005,showlegend=False,hoverinfo='skip',legendgroup='peaks'))
fig3.add_trace(go.Scatter(x=data_ne['pred'].freq,y=-data_ne['pred'].int,name='Transitions',mode='markers',marker_color=color,
                         customdata=data_ne['pred']['label'].to_numpy(),hovertemplate='%{customdata}',legendgroup='pred'))
fig3.add_trace(go.Bar(x=data_ne['pred'].freq,y=-data_ne['pred'].int,width=0.005,showlegend=False,hoverinfo='skip',marker_color=color,legendgroup='pred'))
fig3.update_layout(
    xaxis_title="Frequency (MHz)",
    yaxis_title="Intensity (AU)",
)
fig3.update_xaxes(tickformat='digit')
v = pt.__version__.split('.')
if int(v[0])>=5:
    if int(v[0]) == 5 and int(v[1]) < 17:
        fig3.update_yaxes(range=[-0.3,0.3])
    else:
        fig3.update_yaxes(range=[-0.3,0.3],autorangeoptions={'minallowed':-0.3,'maxallowed':0.3})
        




tab1, tab2, tab3 = st.tabs(["1 bar Ar", "3.75 bar Ar", "3.75 bar Ne - Isotopologues"])

with tab1:
    st.plotly_chart(fig1,use_container_width=True,config = {'scrollZoom': True})
    st.dataframe(data_0psi['pred'].drop('label',axis=1),use_container_width=True)
    
with tab2:
    st.plotly_chart(fig2,use_container_width=True,config = {'scrollZoom': True})
    st.dataframe(data_40psi['pred'].drop('label',axis=1),use_container_width=True)
    
with tab3:
    st.plotly_chart(fig3,use_container_width=True,config = {'scrollZoom': True})
    st.dataframe(data_ne['pred'].drop('label',axis=1),use_container_width=True)