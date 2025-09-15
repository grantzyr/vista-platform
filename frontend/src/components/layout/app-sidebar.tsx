import { useEffect, useState } from 'react'
import { useLocation, useRouter } from '@tanstack/react-router'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarRail,
} from '@/components/ui/sidebar'
import { NavGroup } from '@/components/layout/nav-group'
import { sidebarData } from './data/sidebar-data'

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const [showBar, setShowSidebar] = useState(true)
  const router = useRouter()
  const location = useLocation()

  useEffect(() => {
    const path = location.pathname
    if (path.startsWith('/start-game') || path.startsWith('/session-detail') || path.startsWith('/benchmarks')) {
      setShowSidebar(false)
    } else {
      setShowSidebar(true)
    }
  }, [location]);

  return (
    <div className='flex flex-col'>
      <div className='flex flex-1'>
        {showBar && (
          <Sidebar collapsible='icon' variant='floating' {...props}>
            
            <SidebarContent>
              {sidebarData.navGroups.map((props) => (
                <NavGroup key={props.title} {...props} />
              ))}
            </SidebarContent>
            <SidebarFooter>
              <button
                className='bg-primary mt-2 w-full rounded py-2 text-white'
                onClick={() => {
                  setShowSidebar(false)
                  router.navigate({ to: '/start-game' }) 
                }}
              >
                START
              </button>
            </SidebarFooter>
            <SidebarRail />
          </Sidebar>
        )}
      </div>
    </div>
  )
}
