import { Button, DarkThemeToggle, Navbar, NavbarBrand } from "flowbite-react";

function ShortNavbar() {
  return (
    <nav className="fixed z-30 w-full border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
      <Navbar fluid rounded>
        <NavbarBrand href="https://google.com">
          <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
            Short
          </span>
        </NavbarBrand>
        <div className="flex space-x-2 md:order-2">
          <DarkThemeToggle />
          <Button>Create short URL</Button>
        </div>
      </Navbar>
    </nav>
  );
}

export default ShortNavbar;
