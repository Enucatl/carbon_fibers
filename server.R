library(shiny)
library(ggplot2)
library(data.table)

shinyServer(function(input, output) {

  dataset <- reactive(function() {
    data.table(read.csv(input$file), key="angle")
  })

  output$plot <- reactivePlot(function() {

    min_pixel <- input$min_pixel
    max_pixel <- input$max_pixel

    absorption.table <- dataset()[pixel %between% c(min_pixel, max_pixel),
                                    list(signal="absorption",
                                        mean=mean(absorption),
                                        sd=sd(absorption)),
                                    by=angle]
    darkfield.table <- dataset()[pixel %between% c(min_pixel, max_pixel),
                                list(signal="darkfield",
                                        mean=mean(darkfield),
                                        sd=sd(darkfield)),
                                    by=angle]

    average <- rbind(absorption.table, darkfield.table)
    graph <- ggplot(average,
                aes(x=angle,
                    y=mean,
                    color=signal)) + geom_line(
                aes(group=signal)) + scale_y_continuous(
                name=sprintf("average over pixels %d to %d",
                    min_pixel, max_pixel)) + scale_x_continuous(
                name="angle (degrees)")
    if (input$sd)
      graph <- graph + geom_ribbon(
                    aes(ymin=mean - sd,
                        ymax=mean + sd,
                        linetype=NA,
                        fill=signal),
                    alpha=0.2)

    print(graph)

  }, height=700)

})
