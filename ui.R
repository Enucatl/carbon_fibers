library(shiny)
library(ggplot2)

dataset <- diamonds

shinyUI(pageWithSidebar(

  headerPanel("Angular dependence of dark field signal"),

  sidebarPanel(
    includeCSS("sidebar.css"),

    sliderInput('pixels', 'Average over pixels', min=1, max=1024,
                value=c(500, 550), step=1, round=0),

    selectInput('file', 'File', list.files(path=".",
                                           pattern="*.csv")),

    checkboxInput('sd', 'Show standard deviation the selected pixels')

  ),

  mainPanel(
    plotOutput('plot')
  )
))
