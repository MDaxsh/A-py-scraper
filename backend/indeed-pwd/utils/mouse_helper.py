"""
============================================================
MOUSE HELPER
============================================================
Simulates human-like mouse movements to avoid bot detection.
Uses random curves and delays to appear more natural.
============================================================
"""

import asyncio
import random
import math


class MouseHelper:
    """
    Helper class for simulating human-like mouse movements.
    
    Usage:
        mouse = MouseHelper(page)
        await mouse.move_to_element(element)
        await mouse.human_click(element)
    """
    
    def __init__(self, page):
        """
        Initialize with a Playwright page instance.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.current_x = random.randint(100, 500)
        self.current_y = random.randint(100, 300)
    
    async def random_mouse_move(self):
        """
        Move mouse to a random position on the page.
        Simulates idle mouse movement.
        """
        target_x = random.randint(100, 1000)
        target_y = random.randint(100, 600)
        await self.move_to(target_x, target_y)
    
    async def move_to(self, target_x: int, target_y: int, steps: int = None):
        """
        Move mouse from current position to target using a curved path.
        
        Args:
            target_x: Target X coordinate
            target_y: Target Y coordinate
            steps: Number of steps (auto-calculated if None)
        """
        if steps is None:
            # Calculate steps based on distance - fewer steps for faster movement
            distance = math.sqrt((target_x - self.current_x)**2 + (target_y - self.current_y)**2)
            steps = max(5, int(distance / 50))  # Reduced from /20 to /50
        
        # Generate curved path points using bezier-like curve
        points = self._generate_curve_points(
            self.current_x, self.current_y,
            target_x, target_y,
            steps
        )
        
        # Move through each point with minimal delays
        for x, y in points:
            await self.page.mouse.move(x, y)
            # Very fast movement (1-5ms per step)
            await asyncio.sleep(random.uniform(0.001, 0.005))
        
        self.current_x = target_x
        self.current_y = target_y
    
    def _generate_curve_points(self, start_x, start_y, end_x, end_y, steps):
        """
        Generate points along a curved path (quadratic bezier).
        Adds natural-looking curvature to mouse movement.
        """
        points = []
        
        # Random control point for bezier curve (creates natural arc)
        ctrl_x = (start_x + end_x) / 2 + random.randint(-100, 100)
        ctrl_y = (start_y + end_y) / 2 + random.randint(-100, 100)
        
        for i in range(steps + 1):
            t = i / steps
            
            # Quadratic bezier formula
            x = (1-t)**2 * start_x + 2*(1-t)*t * ctrl_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * ctrl_y + t**2 * end_y
            
            # Add tiny random jitter for human-like imprecision
            x += random.uniform(-2, 2)
            y += random.uniform(-2, 2)
            
            points.append((int(x), int(y)))
        
        return points
    
    async def move_to_element(self, element):
        """
        Move mouse to a page element with human-like movement.
        
        Args:
            element: Playwright locator or element
        """
        try:
            box = await element.bounding_box()
            if box:
                # Target slightly random position within element
                target_x = box['x'] + box['width'] * random.uniform(0.3, 0.7)
                target_y = box['y'] + box['height'] * random.uniform(0.3, 0.7)
                await self.move_to(int(target_x), int(target_y))
        except:
            pass
    
    async def human_click(self, element):
        """
        Click an element with human-like behavior:
        1. Move mouse to element with curve
        2. Small pause before clicking
        3. Random click duration
        
        Args:
            element: Playwright locator or element
        """
        # Move to element first
        await self.move_to_element(element)
        
        # Brief pause before clicking (50-100ms)
        await asyncio.sleep(random.uniform(0.05, 0.1))
        
        # Quick click (30-70ms press duration)
        await self.page.mouse.down()
        await asyncio.sleep(random.uniform(0.03, 0.07))
        await self.page.mouse.up()
    
    async def human_type(self, element, text: str, click_first: bool = True):
        """
        Type text into an element with human-like behavior:
        1. Click the element
        2. Type with random delays between keystrokes
        
        Args:
            element: Playwright locator or element
            text: Text to type
            click_first: Whether to click element before typing
        """
        if click_first:
            await self.human_click(element)
            await asyncio.sleep(random.uniform(0.1, 0.2))
        
        # Type each character with realistic typing speed (30-80ms per char)
        for char in text:
            await element.press(char)
            await asyncio.sleep(random.uniform(0.03, 0.08))
    
    async def scroll_naturally(self, amount: int = None):
        """
        Scroll the page in a human-like manner.
        
        Args:
            amount: Pixels to scroll (random if None)
        """
        if amount is None:
            amount = random.randint(100, 300)
        
        # Scroll in chunks
        direction = 1 if amount > 0 else -1
        remaining = abs(amount)
        
        while remaining > 0:
            scroll_step = min(remaining, random.randint(80, 150))
            await self.page.mouse.wheel(0, scroll_step * direction)
            remaining -= scroll_step
            await asyncio.sleep(random.uniform(0.02, 0.05))
    
    async def idle_movement(self, duration: float = 0.5):
        """
        Simulate brief idle mouse movement.
        Makes small random movements like a human would.
        
        Args:
            duration: How long to simulate idle movement (seconds)
        """
        end_time = asyncio.get_event_loop().time() + duration
        
        while asyncio.get_event_loop().time() < end_time:
            # Small random movement
            new_x = self.current_x + random.randint(-30, 30)
            new_y = self.current_y + random.randint(-20, 20)
            
            # Keep within reasonable bounds
            new_x = max(50, min(1200, new_x))
            new_y = max(50, min(700, new_y))
            
            await self.move_to(new_x, new_y, steps=3)
            await asyncio.sleep(random.uniform(0.1, 0.2))
