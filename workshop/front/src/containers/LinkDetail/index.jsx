import React from 'react'
import PropTypes from 'prop-types';

import LinkDetailComponent from '../../components/LinkDetail'

export default class LinkDetail extends React.Component {
  static propTypes = {
    links: PropTypes.array
  }

  render() {
    const { links } = this.props;
    return (
      <LinkDetailComponent links={links} />
    )
  }
}
