import { ListItem } from "@material-ui/core";
import React from "react";

export const ListItemLink = (props: any) => {
    return <ListItem button component="a" {...props} />;
};
