import React from 'react'
import { render } from 'react-dom'
import App from '../containers/App'

window.render_components = properties => {
  window.params = {...properties};
  render(<App/>, document.getElementById('app'));
};

if (module.hot) {
  if (window.params) window.render_components(window.params);
  module.hot.accept();
}
