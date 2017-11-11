import React from 'react'
import { render } from 'react-dom'
import LinksDetail from '../containers/LinksDetail'

window.render_components = properties => {
  window.params = {...properties};
  render(<LinksDetail links={properties.links}/>, document.getElementById('app'));
};

if (module.hot) {
  if (window.params) window.render_components(window.params);
  module.hot.accept();
}
