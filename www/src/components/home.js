import React, { Component } from "react";
import {
    Container,
    Divider,
    Segment,
    Grid,
    Table,
    Button,
    Message,
} from "semantic-ui-react";
import { NavLink } from "react-router-dom";


export default class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            hint: false,
            selected: false,
            display: false,
            locked: false,
        };
    }

    render() {
        return (
            <Container fluid>
                <Message>Welcome to project NYX! Click below to find something new to watch!</Message>
                <Grid>
                    <Grid.Column width={8}>
                        <Button huge to={"/lovers"} fluid
                            as={NavLink}>For movie lovers</Button>
                    </Grid.Column>
                    <Grid.Column width={8}>
                        <Button huge to={"/lovers"} fluid
                            as={NavLink}>For movie producers</Button>
                    </Grid.Column>
                </Grid>

            </Container>
        )
    }
}
