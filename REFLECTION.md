For this assignment, I chose to use the freely available [Open Meteo API](https://open-meteo.com/)  
to create a basic weather forecasting service based on ZIP code.  
I looked into several weather APIs; however, many required API tokens.  
To keep setup complexity minimal for reviewers, I skipped those and stuck with Open Meteo.  

The app started without a sidebar.  
Initially, everything was in one giant vertical layout, which quickly proved unsustainable.  
I explored various display methods and bounced ideas off Claude to see different iterations.  
Ultimately, I settled on using a sidebar for input and dedicating the main container solely to displaying data.  

While building the main container, I realized the vertical-content trap was looming again—  
especially for weather forecasting, where a linear flow is key to maintaining context.  
I recalled the tabs we used in the HCI Testing Tool (Project 1) and, after methodical iteration,  
implemented a metric-per-tab setup that met my performance and usability expectations.  

Working with Open Meteo was straightforward.  
I knew from the start I’d use ZIP-code input.  
The API provides an easy ZIP-to-latitude/longitude lookup (though each “point” can cover a broad area,  
which is why my map defaults to Miami’s center).  
Translating the returned data into the metrics I needed was seamless,  
and then I moved on to designing the display.  

I spent the most time fine-tuning the display format.  
Originally, I relied on Streamlit’s built-in charts (Vega), but quickly grew dissatisfied with their presentation.  
After testing various chart types, I landed on Matplotlib.  
While the final graphs aren’t as polished as the React-based charts I’m used to building,  
they proved far more readable and flexible than the default Streamlit charts.  

Overall, this was a fun project for experimenting with a basic UI for weather data.  
Streamlit—while limited in customization—offers simple, intuitive ways to build data displays.  
With more tinkering, I’m confident I could overcome its limitations and create a world-class UI for this app.  
For now, I’m satisfied with the features and functionality I delivered.  
This project was also a great exercise in time management and taking an idea from start to finish.  
