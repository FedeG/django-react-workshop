import React from 'react';
import App from './index.jsx';
import { shallow } from 'enzyme';

describe('App Component', () => {

  describe('#render', () => {

    it('should render the component properly', () => {
      const wrapper = shallow(<App id="id" audioPath="path"/>);
      const componentInDOM = '<div class="container"><div class="row"><div class="col-sm-12"><h1>Sample App!</h1></div></div></div>';
      expect(wrapper.html()).toBe(componentInDOM);
    })

  })

})
