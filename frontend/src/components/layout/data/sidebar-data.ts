import { type SidebarData } from '../types'

export const sidebarData: SidebarData = {
  user: {
    name: 'satnaing',
    email: 'satnaingdev',
    avatar: '/avatars/shadcn.jpg',
  },
  navGroups: [
    {
      title: 'General',
      items: [
        {
          title: 'Providers',
          url: '/providers',
        },
        
        {
          title: 'Models',
          url: '/models',
        },
        {
          title: 'Dataset',
          url: '/dataset',
        },
        {
          title: 'History',
          url: '/history',
        },
        
      ],
    },
  ],
}
