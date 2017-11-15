import React from 'react'
import PropTypes from 'prop-types';
import Websocket from 'react-websocket';

import LinksDetailComponent from '../../components/LinksDetail'
import { LINKS_API_URL, LINKS_WS_URL } from '../../utils/urls'
import { getUrl } from '../../utils/api'


export default class LinksDetail extends React.Component {
  static propTypes = {
    links: PropTypes.array.isRequired
  }

  constructor(props) {
    super(props);
    const { links } = this.props;
    this.state = {
      links: [...links]
    }
  }

  getLink = (id, fields) => {return {id, fields}};

  _onRefresh = () => {
    getUrl(LINKS_API_URL)
      .then(newLinks => {
        const links = newLinks.map(link => this.getLink(link.id, link));
        this.setState({links});
      })
  }

  _onUpdate = event => {
    const { links } = this.state;
    const {payload: {action, data, pk}} = JSON.parse(event);
    let newLinks = [...links];
    switch (action) {
      case 'update':
        newLinks = newLinks.map(link => {
          if (link.pk === pk) return this.getLink(pk, data);
          return link;
        })
        break;
      case 'create':
        newLinks.push(this.getLink(pk, data))
        break;
     case 'delete':
        newLinks = newLinks.filter(link => link.pk !== pk);
        break;
    }
    this.setState({links: newLinks});
  }

  render() {
    const { links } = this.state;
    return (
      <div>
        <LinksDetailComponent links={links} onRefresh={this._onRefresh}/>
        <Websocket url={LINKS_WS_URL} onMessage={this._onUpdate}/>
      </div>
    )
  }
}
