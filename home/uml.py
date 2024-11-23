from graphviz import Digraph

# Create a UML Diagram
uml = Digraph(format='png', filename='uml_budget_tracker')
uml.attr(rankdir='TB', size='8,10')

# Nodes for the UML
uml.node("User", shape="actor", label="User")
uml.node("Frontend", shape="component", label="Frontend\n(HTML, CSS, JS)")
uml.node("Backend", shape="component", label="Backend\n(Django, Python)")
uml.node("Database", shape="cylinder", label="Database\n(SQLite)")

# Relationships
uml.edge("User", "Frontend", label="Interacts with")
uml.edge("Frontend", "Backend", label="Sends Requests (RESTful API)")
uml.edge("Backend", "Database", label="Queries/Updates")
uml.edge("Database", "Backend", label="Returns Data")
uml.edge("Backend", "Frontend", label="Responds with Data/Results")

# Render the UML diagram
uml_filepath = 'uml_budget_tracker.png'
uml.render(uml_filepath, cleanup=True)
uml_filepath
