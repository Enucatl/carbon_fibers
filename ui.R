library(shiny)
library(ggplot2)

dataset <- diamonds

shinyUI(pageWithSidebar(

  headerPanel("Angular dependence of dark field signal"),

  sidebarPanel(

    sliderInput('min_pixel', 'From Pixel', min=1, max=1024,
                value=500, step=1, round=0),
    sliderInput('max_pixel', 'To Pixel', min=1, max=1024,
                value=510, step=1, round=0),

    selectInput('file', 'File', list.files(path=".",
                                           pattern="*.csv")),

    checkboxInput('sd', 'Show standard deviation'),

  ),

  mainPanel(
    plotOutput('plot')
  )
))
