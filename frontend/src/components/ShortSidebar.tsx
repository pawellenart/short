import {
  Sidebar,
  SidebarItem,
  SidebarItemGroup,
  SidebarItems,
} from "flowbite-react";
import { HiLink } from "react-icons/hi2";

function ShortSidebar() {
  return (
    <aside className="transition-width fixed left-0 top-0 z-20 flex h-full w-64 flex-shrink-0 flex-col pt-16 font-normal duration-75 lg:flex">
      <Sidebar>
        <SidebarItems>
          <SidebarItemGroup>
            <SidebarItem href="/" icon={HiLink}>
              Links
            </SidebarItem>
          </SidebarItemGroup>
        </SidebarItems>
      </Sidebar>
    </aside>
  );
}

export default ShortSidebar;
