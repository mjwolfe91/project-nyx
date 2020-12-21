import React, { Component } from "react";
import {
    Container,
    Menu,
    Embed,
    Grid,
    Segment
} from "semantic-ui-react";

export default class Producers extends Component {
    constructor(props) {
        super(props);
        this.links = {
            'Reviewer Gender and Genre': 'https://statsthroughsimulation.shinyapps.io/GenreGender/',
            'Ratings Over Time by Genre': '/genre_ratings.html',
            'Ratings by Demographic': 'https://sachinac.shinyapps.io/nyx_project/',
            'Bechdel Analysis': 'bechdel_analysis.html',
            'Movies by Genre': '/genres.html',
            'Overall Ratings distribution': '/ratings.html',

        }

        this.state = {
            activeItem: 'Reviewer Gender and Genre',
        };
    }

    render() {
        let menuItems = [];
        for (const key of Object.keys(this.links)) {
            const text = key.toString()
            menuItems.push(
                <Menu.Item
                    name={text}
                    key={text}
                    active={this.state.activeItem === text}
                    onClick={(e, { name }) => this.setState({ activeItem: name })}
                />
            )
        }

        return (
            <Container fluid>
                <Grid>
                    <Grid.Column width={3}>
                        <Menu vertical attached>
                            {menuItems}
                        </Menu>
                    </Grid.Column>

                    <Grid.Column width={13}>
                        <Segment style={{ overflow: 'auto', height: window.innerHeight * 0.9 }} >
                            <iframe src={this.links[this.state.activeItem]} title="Data Browser" width='100%' height='100%' frameBorder="0" />
                            {/* <Embed active={true}
                                url={this.links[this.state.activeItem]}
                                onUpdate={(e) => console.log(e)} /> */}
                        </Segment>
                    </Grid.Column>
                </Grid>
            </Container >

        )
    }
}
