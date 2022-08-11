A Lightning App demo of hierarchical jobs with interactive control on parallelism.  Dunamic research flow and ealstic production pipeliens are possible with Lighting App. 

Techniques demonstrated:
- Flows within Flow..
- Flow with dynamic number of Works within.
- Works starting and shutting dynamically.
- A work starts when there is something to run.
- Work terminates after specified number of idle time to save cost.
- Work has active terminal while running for debugging.
- UI is dynamically generated.

# The Demo Arch

A Flow has two two Flows within it.
```mermaid
graph TD
Flow1
Flow2
Flow1 -->|>3 iters completed| Flow3
Flow2 -->|>6 iters completed| Flow3
subgraph Start if Conditions are met
    Flow3
end
```

Each Flow has elastic (scale out and scale in) number of Works.
```mermaid
graph TD
UI --> |Interactive Control During the Run| Run
Run --> Work0
Run --> Work1
Run --> WorkN
subgraph Number increase and decrease dynamically  
		Work0
		Work1
		WorkN
end
```

# Screen shots

Work has active terminal while running for debugging.

![Terminal](static/terminal.png)

A work starts when there is something to run.

![job control](static/jobs.png)

It terminates after specified number of idle time to save cost.

![terminate](static/elastic.png)

UI is dynamically generated.
![dyamic](static/progress.png)

