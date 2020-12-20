import React, { Component } from "react";
import {
    Container,
    Card,
    Placeholder,
    Grid,
    Table,
    Button,
    Message,
} from "semantic-ui-react";

export default class Lovers extends Component {
    constructor(props) {
        super(props);
        this.state = {
            locked: false,
        };
    }

    render() {
        return (
            <Container fluid align='center'>
                <Message>#TODO: Implement the workflow</Message>
                <Card.Group itemsPerRow={3}>
                    <Card >
                        <Card.Content>
                            <Placeholder>
                                <Placeholder.Image rectangular />
                            </Placeholder>
                        </Card.Content>
                    </Card>
                    <Card>
                        <Card.Content>
                            <Placeholder>
                                <Placeholder.Image rectangular />
                            </Placeholder>
                        </Card.Content>
                    </Card>
                    <Card>
                        <Card.Content>
                            <Placeholder>
                                <Placeholder.Image rectangular />
                            </Placeholder>
                        </Card.Content>
                    </Card>
                </Card.Group>
                <Grid ncols={2}>
                    <Grid.Column width={8}>
                        <Button huge>Last Pick</Button>
                    </Grid.Column>
                    <Grid.Column width={8} textAlign='right'>
                        <Button huge>Next Pick</Button>
                    </Grid.Column>
                </Grid>

            </Container>
        )
    }
}
