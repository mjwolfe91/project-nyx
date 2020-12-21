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

export default class Producers extends Component {
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
                <Divider horizontal />
                <Grid ncols={2}>
                    <Grid.Column>
                        <Button huge>For movie lovers</Button>
                    </Grid.Column>
                    <Grid.Column>
                        <Button huge>For movie producers</Button>
                    </Grid.Column>
                </Grid>

            </Container>
        )
    }
}
