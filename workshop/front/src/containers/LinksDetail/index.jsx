import React from 'react'
import PropTypes from 'prop-types';

import LinksDetailComponent from '../../components/LinksDetail'

export default class LinksDetail extends React.Component {
  static propTypes = {
    links: PropTypes.array
  }

  render() {
    const { links } = this.props;
    return (
      <LinksDetailComponent links={links} />
    )
  }
}
