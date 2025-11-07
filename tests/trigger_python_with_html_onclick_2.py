from nicegui import ui

def luW(event):
    # whatever we sent from the browser is available as event.args
    payload = event.args
    print(type(payload))
    print('Server received payload:', payload)
    ui.notify(f"Server got: {payload}")

# listen for custom event "luW"
ui.on('luW', luW)

ui.html('''
<div style="padding:20px">
  <ul>
    <li>
      <a href="#" onclick="emitEvent('luW', 'Product A'); return false;">Product A (string)</a>
    </li>
    <li>
      <a href="#" onclick="emitEvent('luW', {id: 2, name: 'Product B'}); return false;">
        Product B (object)
      </a>
    </li>
    <li>
      <a href="#" onclick="emitEvent('luW', ['331049','70320','70639']); return false;">
        Product C (object with array)
      </a>
    </li>
    <li>
      <a href="#" onclick="emitEvent('luW', {id: 3, codes: ['331049','70320','70639']}); return false;">
        Product D (object with array)
      </a>
    </li>
  </ul>
</div>
''', sanitize=False)

ui.run(port=9999)
