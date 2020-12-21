import React, { Component } from "react";
import {
    Container,
    Transition,
    Grid,
    Button,
    Message,
    Divider,
    Rating,
    Search,
    Image
} from "semantic-ui-react";
import get from 'axios';

export default class Lovers extends Component {
    constructor(props) {
        super(props);
        this.state = {
            endPage: 4,
            currentPage: 0,
            ratings: [],
            rating: 0,
            movieTitle: '',
            recs: [],
            resultsReady: false
        };

        for (const _ in [...Array(this.state.endPage).keys()]) {
            this.state.ratings.push(
                {
                    rating: 0,
                    movieTitle: ''
                }
            )
        }
    }

    updateReviews = i => {
        this.setState(state => {
            const ratings = state.ratings.map((item, j) => {
                if (j === i) {
                    return {
                        rating: this.state.rating,
                        movieTitle: this.state.movieTitle
                    };
                } else {
                    return item;
                }
            });
            return {
                ratings,
            };
        });
    }

    getRecommendations = async () => {
        let res = await get("https://www.projectnyx.org/sqlapi/autocomplete", { params: { incoming: this.state.movieTitle } });
        const results = res.data.map(x => { return ({ title: x }) })
        this.setState({ recs: results });
    }


    sleep = async (ms) => {
        await new Promise(resolve => setTimeout(resolve, ms));
    }

    nextPage = () => {
        const currentPage = this.state.currentPage;
        this.updateReviews(currentPage);
        this.setState({ currentPage: currentPage + 1 })
        this.loadPage()
    }

    backPage = () => {
        const currentPage = this.state.currentPage;
        this.updateReviews(currentPage);
        this.setState({ currentPage: currentPage - 1 })
        this.loadPage()
    }

    loadPage = () => {
        let { rating, movieTitle } = this.state.ratings[this.state.currentPage];
        this.setState({
            rating: rating,
            movieTitle: movieTitle
        });
    }

    componentDidMount() {
        this.loadPage();
    }

    render() {
        console.log(this.state.ratings);
        return (
            <Container align='center' >
                <Message>Select movies and rate them so we can make recommendations!</Message>
                <Divider hidden />
                <Search
                    huge
                    results={this.state.recs}
                    onSearchChange={(e) => {
                        console.log(e.target.value);
                        this.setState({ movieTitle: e.target.value });
                        this.getRecommendations()
                    }}
                    onResultSelect={(e, data) => {
                        this.setState({ movieTitle: data.result.title });
                    }}
                    value={this.state.movieTitle}
                    placeholder="Find your movie here."
                />
                <Divider hidden />
                <Rating icon='star' size='massive' maxRating={5} value={this.state.rating}
                    onRate={(e, { rating }) => {
                        console.log(rating);
                        this.setState({ rating: rating });
                    }} />
                <Divider hidden />
                <Grid>
                    {/* <Grid.Column width={3} floated='left'>
                        <Button huge disabled={this.state.currentPage === 0} onClick={this.backPage}>Last Pick</Button>
                    </Grid.Column> */}
                    <Grid.Column width={1} floated='center'>
                        <Message floating compact>{this.state.currentPage + 1}</Message>
                    </Grid.Column>
                    <Grid.Column width={3} floated='right'>
                        <Transition visible={this.state.currentPage === this.state.endPage} animation='slide' duration={500}>
                            <Button huge onClick={() => this.setState({ resultsReady: true })}>Get My Results!</Button>
                        </Transition>
                        <Transition visible={this.state.currentPage != this.state.endPage} animation='slide' duration={500}>
                            <Button huge disabled={this.state.currentPage === this.state.endPage} onClick={this.nextPage}>Next Pick</Button>
                        </Transition>
                    </Grid.Column>
                </Grid>
                <Transition visible={this.state.resultsReady} animation='slide' duration={5000}>
                    <Container fluid>
                        <Divider horizontal>We Recommend</Divider>
                        <Image size='large' src='/turtle.jpg' />
                    </Container>
                </Transition>
            </Container>
        )
    }
}
