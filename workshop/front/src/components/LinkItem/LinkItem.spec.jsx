import React from 'react';
import LinkItem from './index.jsx';
import { shallow } from 'enzyme';

describe('LinkItem Component', () => {
  let link;

  beforeAll(() => {
    link = {
      model: 'links.link',
      pk: 1,
      fields: {
        name: 'Gitlab with workshop',
        url: 'https://gitlab.com/FedeG/django-react-workshop/',
        pending: false,
        description: '',
        user: 1
      }
    }
  })

  describe('props', () => {

    it('should declare propsTypes', () => {
      expect(Object.keys(LinkItem.propTypes)).toHaveLength(1);
      expect(LinkItem.propTypes).toHaveProperty('link');
    })

  })

  describe('#render', () => {

    it('should render the component properly', () => {
      const wrapper = shallow(<LinkItem link={link}/>);
      const componentInDOM = `<p>${link.fields.name}: <a href="${link.fields.url}">${link.fields.url}</a></p>`;
      expect(wrapper.html()).toBe(componentInDOM);
    })

  })

})
