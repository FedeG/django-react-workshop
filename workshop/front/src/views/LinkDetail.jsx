import React from 'react'
import { render } from 'react-dom'
import LinkDetail from '../containers/LinkDetail'

window.render_components = properties => {
  window.params = {...properties};
  render(<LinkDetail links={properties.links}/>, document.getElementById('app'));
};

if (module.hot) {
  if (window.params) window.render_components(window.params);
  module.hot.accept();
}
