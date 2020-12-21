import React, { Component } from "react";
import { Menu } from "semantic-ui-react";
import { NavLink } from "react-router-dom";

export default class Header extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeItem: 'project nyx'
        };
    }
    handleItemClick = (e, { name }) => this.setState({ activeItem: name });

    render() {
        const activeItem = this.state.activeItem;

        return (
            <Menu attached>
                <Menu.Item
                    name="project nyx"
                    active={activeItem === "project nyx"}
                    onClick={this.handleItemClick}
                    to={"/"}
                    as={NavLink}
                    exact
                />
                <Menu.Item
                    position="right"
                    name="lovers"
                    active={activeItem === "lovers"}
                    onClick={this.handleItemClick}
                    to={"/lovers"}
                    as={NavLink}
                    exact
                />
                <Menu.Item
                    name="producers"
                    active={activeItem === "producers"}
                    onClick={this.handleItemClick}
                    to={"/producers"}
                    as={NavLink}
                    exact
                />
            </Menu>
        );
    }
}
