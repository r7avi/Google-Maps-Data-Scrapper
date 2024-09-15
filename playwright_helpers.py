async def get_element_text(page, selector, timeout=30000):
    try:
        element = page.locator(selector)
        if await element.count() > 0:
            return await element.inner_text(timeout=timeout)
        return ''
    except Exception as e:
        print(f"Error getting text for selector {selector}: {e}")
        return ''

async def get_element_attribute(page, selector, attribute, timeout=30000):
    try:
        element = page.locator(selector)
        if await element.count() > 0:
            return await element.get_attribute(attribute, timeout=timeout)
        return ''
    except Exception as e:
        print(f"Error getting attribute {attribute} for selector {selector}: {e}")
        return ''
