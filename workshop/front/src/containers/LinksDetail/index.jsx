import React from 'react'
import PropTypes from 'prop-types';

import LinksDetailComponent from '../../components/LinksDetail'
import { LINKS_API_URL } from '../../utils/urls'
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


  _onRefresh = () => {
    getUrl(LINKS_API_URL)
      .then(newLinks => {
        const links = newLinks.map(link => {
          return {
            pk: link.id,
            fields: link
          }
        });
        this.setState({links});
      })
  }

  render() {
    const { links } = this.state;
    return (
      <LinksDetailComponent links={links} onRefresh={this._onRefresh}/>
    )
  }
}
