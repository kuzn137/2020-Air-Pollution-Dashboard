import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`
file_name = 'data//waqi-covid19-airqualitydata-2020.csv'
particles = ['pm25', 'pm10', 'no2', 'o3', 'so2']
df = pd.read_csv(file_name, skiprows=[0,1,2,3])
def prepare_monthly(dfn):
        """
        args:
          None
        returns: 
           array of median data per month over all countries for each of chosen particles
        """     
        dfn['month']=dfn['Date'].apply(lambda x: int(x.split('-')[1]))
        dfn= dfn.loc[dfn['month']<9].copy()
        df1=dfn.drop(['Date'], axis=1)
        return df1
df = prepare_monthly(df)
class prepare_data():
    def __init__(self, df):
        self.df = df
     
    def prepare_monthlydata(self, df1):
        #median data per month over all countries
        dfmm = df1.groupby(['month', 'Specie'], as_index=False)['median'].median()
        return dfmm
    def prepare_countrymed(self, specie):
        """
        args:
          specie
        returns: 
           dataframe with median concentration of chosen specie over all time for each country
        """     
        dfcm = self.df[self.df['Specie']==specie].groupby(['Country'], as_index=False)['median'].median().sort_values(by='median')
        return dfcm
    def particles_monthly_country(self, country):
        """
        args: country name
        returns: data_frame with monthly medians for given country for each specie
        """
        dftemp = self.df[self.df['Country']==country] 
        
        dfm=self.prepare_monthlydata(dftemp)
        return dfm
def plot(df):
    '''
    args: dataframe
    returns graph
    '''
    graph=[]
    for particle in particles:
        x_val = df[df['Specie'] == particle].month.tolist()
        y_val =  df.loc[df['Specie'] == particle, 'median'].tolist()
        graph.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = particle
          )
         )
    return graph
    
   
    

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    particles = ['pm25', 'pm10', 'no2', 'o3', 'so2']  
    df1 = prepare_data(df).prepare_monthlydata(df)
    graph_one = plot(df1)
    layout_one = dict(title = 'All countries',
                xaxis = dict(title = 'Month',
                tickmode = 'array',
                tickvals = [2, 4, 6, 8],
                ticktext = ['Feb', 'Apr', 'Jun', 'Aug']),
                 # autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'Median concentration'),
                )
    
    dfcn = prepare_data(df).particles_monthly_country('CN')
    graph_two =plot(dfcn)
    layout_two = dict(title = 'China, great job!',
                xaxis = dict(title = 'Month',
                tickmode = 'array',
                tickvals = [2, 4, 6, 8],
                ticktext = ['Feb', 'Apr', 'Jun', 'Aug']),
                yaxis = dict(title = 'Median concentration'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    
    dfus = prepare_data(df).particles_monthly_country('US')
    graph_three = plot(dfus)
   

    layout_three = dict(title = 'United States',
                xaxis = dict(title = 'Month',
                tickmode = 'array',
                tickvals = [2, 4, 6, 8],
                ticktext = ['Feb', 'Apr', 'Jun', 'Aug']),
                yaxis = dict(title = 'Median concentration')
                       )
    
# fourth chart shows rural population vs arable land
   # dfru = prepare_data(file_name).particles_monthly_country('RU')
    dfpm25=prepare_data(df).prepare_countrymed('pm25')
    dfn = pd.concat([dfpm25[:4], dfpm25[-3:]])
   # graph_four = plot(dfru)
    graph_four=[]
    graph_four.append(
      go.Bar(
      x = dfn.Country.tolist(),
      y =dfn['median'])
    )

    layout_four = dict(title = 'Countries with best and worst concentrations of PM 2.5',     
                xaxis = dict(title = 'Country',  tickmode = 'array',
                tickvals = ['BG', 'CH', 'IS', 'EE', 'ML', 'BD', 'UG'],
                ticktext = ['Bulgaria', 'Switzerland', 'Iceland', 'Estonia', 'Mali', 'Bangladesh', 'Uganda']),
                yaxis = dict(title = 'Median concentration'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures