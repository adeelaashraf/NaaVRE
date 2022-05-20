import { Chip } from '@material-ui/core';
import * as React from 'react';


interface IState {

}

interface GitHubCredPanelProps {
    credentials: []
}

const DefaultState: IState = {

}


export class GitHubCredPanel extends React.Component<GitHubCredPanelProps, IState> {

    state = DefaultState;

    constructor(props: GitHubCredPanelProps) {
        super(props);
    }

    render(): React.ReactElement {
        return (
            <div>
                {this.props.credentials.map(cred =>
                    <Chip label={cred['name']} onClick={() => {}}/>
                )}
            </div>
        )
    }
}