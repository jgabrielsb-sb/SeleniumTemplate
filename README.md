## Selenium Template ##

### 1. Introduction ###

This template emerged by necessity of having a reliable testable selenium environment to serve as background to execute automations. Some problems that I had that are solved by the use of this template:
    
* When downloading files on automations there were some conditions that must be met to succesfully complete the process (the folder must have permissions to be written, per example). At times I would only discover that those pre-conditions were not met on compiling time, what introduced many bugs.

* One problem on Selenium is that some automations can vary on different executions. The problem was that I could not entirely rely on my automations because of that variation. The alternative that I found was to create a structure where I could somehow execute those automations on a reliable interface that could give me good insights, such as:
        - percentage of times that the automation results in sucess;
        - time taken by each action in the automation;
    Those insights allowed me to perceive the bottlenecks on the selenium automation by measuring time between actions and how succesfull a selenium automation is by measuring it's sucess rate.

* By times I needed different environments exposed. For example: on development, the best webdriver to execute is usually the installed local one. On the other side, in production, the best one can be a remote containerized webdriver. Reproducing those different webdrivers and changing between them on a organized, fast and intuite way was hard. 


### 2. What this template offers ###

A structure that can provide a background for your selenium automations to be:
*  more manageable: automations are separated into concepts as Actions, which makes your code easier to extend and to understand;
* more testable: a default selenium process test template is provided with examples. Then, you can learn by that and reproduce on your own implementations;
* more parametrized: if you implement the automations as defined, you can produce reports that will give you insights about the bottlenecks on the automation and the rate of sucess that you process delivers.
* more dinamic: you can easily change different webdrivers and configure it to execute on a specific way that you want. 






