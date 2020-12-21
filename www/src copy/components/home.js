import React, { Component } from "react";
import {
    Container,
    Grid,
    Button,
    Message,
    Image,
    Divider,
    Segment
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
            <Container fluid textAlign='center'>
                <Container background='/bg.png'>
                    <Grid aligned middle>
                        <Grid.Column width={8}>
                            <Divider horizontal>For Movie Lovers</Divider>
                            <Image src='/corn.jpg' to={"/lovers"}
                                as={NavLink} />
                            <Message positive>Find something new to watch</Message>
                        </Grid.Column>
                        <Grid.Column width={8} >
                            <Divider horizontal>For Movie Production Companies</Divider>
                            <Image src='/cam.jpg' to={"/producers"}
                                as={NavLink} />
                            <Message positive>Find new movie ideas</Message>
                        </Grid.Column>
                    </Grid>
                </Container>
            </Container>
        )
    }
}
