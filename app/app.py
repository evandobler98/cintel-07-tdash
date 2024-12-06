# Import necessary libraries
import seaborn as sns  # For data visualization
from faicons import icon_svg  # For including icons in the UI
from shiny import reactive  # For reactivity in the Shiny app
from shiny.express import input, render, ui  # For UI elements and rendering
import palmerpenguins  # Dataset containing penguin data

# Load the penguin dataset
df = palmerpenguins.load_penguins()

# Set up the page title and layout
ui.page_opts(title="Penguins Dashboard: Insights and Trends", fillable=True)

# Define the sidebar with filter controls
with ui.sidebar(title="Customize Your View"):
    # Input slider to filter penguins by body mass
    ui.input_slider(
        "mass", 
        "Filter by Body Mass (grams)", 
        min=2000, 
        max=6000, 
        value=6000, 
        step=100
    )

    # Input checkboxes to select species of penguins
    ui.input_checkbox_group(
        "species",
        "Select Penguin Species to Display",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    # Add a horizontal rule to separate filters from links
    ui.hr()

    # Add useful links with clear descriptions
    ui.h6("Resources and References")
    ui.a("View the Source Code on GitHub", href="https://github.com/evandobler98/cintel-07-tdash", target="_blank")
    ui.a("Explore the Live App", href="https://evandobler98.github.io/cintel-07-tdash/", target="_blank")
    ui.a("Report Issues or Suggestions", href="https://github.com/evandobler98/cintel-07-tdash/issues", target="_blank")
    ui.a("Learn More About PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Start with a Basic Dashboard Template", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")
    ui.a("Visit the Enhanced Penguins Dashboard Example", href="https://github.com/denisecase/pyshiny-penguins-dashboard-express", target="_blank")

# Define a column layout for value boxes
with ui.layout_column_wrap(fill=False):
    # Value box for the number of penguins
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Total Penguins Displayed"

        # Dynamically calculate and render the number of penguins
        @render.text
        def count():
            return f"{filtered_df().shape[0]} penguins selected"

    # Value box for the average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length (mm)"

        # Dynamically calculate and render the average bill length
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box for the average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Depth (mm)"

        # Dynamically calculate and render the average bill depth
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Define a layout with columns for plots and tables
with ui.layout_columns():
    # Card to display scatterplot of bill length vs. depth
    with ui.card(full_screen=True):
        ui.card_header("Relationship Between Bill Length and Depth")

        # Render a scatterplot with seaborn
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Card to display penguin data in a table
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data Table")

        # Render a DataFrame with selected columns
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Define a reactive function to filter the dataset based on user input
@reactive.calc
def filtered_df():
    # Filter by selected species
    filt_df = df[df["species"].isin(input.species())]
    # Further filter by body mass
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
