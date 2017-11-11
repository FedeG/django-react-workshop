import Enzyme from 'enzyme'
import Adapter from 'enzyme-adapter-react-16'

Enzyme.configure({ adapter: new Adapter() })

global.gettext = jest.fn(text => text)
global.$ = jest.fn()
