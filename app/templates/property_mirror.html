<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Detalles de la Propiedad</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 h-screen flex flex-col">

  <!-- Header -->
  <header class="bg-white shadow flex items-center justify-between px-6 py-4">
    <h1 class="text-xl font-semibold text-gray-700">Detalles de la Propiedad</h1>
    <div class="flex items-center space-x-4 ml-auto">
      <!-- Botones de navegación -->
      <a href="{{ url_for('main.owner_dashboard') }}" 
         class="bg-gray-500 text-white px-6 py-2 rounded-md hover:bg-gray-600 transition-all text-sm">
        Volver al Dashboard
      </a>
      <a href="javascript:history.back()" 
         class="bg-gray-300 text-white px-6 py-2 rounded-md hover:bg-gray-400 transition-all text-sm">
        Volver Atrás
      </a>
      
      <!-- Botón Salir, alineado a la derecha -->
      <form action="{{ url_for('main.logout') }}" method="POST">
        <button type="submit" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-all text-sm">
          Salir
        </button>
      </form>
    </div>
  </header>

  <!-- Detalles de la propiedad -->
  <main class="p-6 overflow-auto space-y-6 flex-grow">
    <div class="bg-white rounded-lg shadow p-6 space-y-4">
      <h2 class="text-lg font-semibold text-gray-800">{{ property.type }} en {{ property.city }}</h2>
      <p class="text-gray-600 mt-2">Precio: ${{ property.price }}</p>
      <p class="text-gray-600 mt-2">Dirección: {{ property.address }}</p>
      <p class="text-gray-600 mt-2">{{ property.description }}</p>
    </div>

    <!-- Mostrar fotos de la propiedad -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {% for photo in photos %}
        <div class="bg-white shadow-lg p-4 rounded-lg">
          <img src="{{ photo.url }}" alt="Foto de la propiedad" class="w-full h-48 object-cover rounded-lg">
        </div>
      {% endfor %}
    </div>

    <!-- Botones de acción -->
    <div class="mt-6 flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 justify-center">
      <!-- Agendar visita -->
      <a href="{{ url_for('main.schedule_visit', property_id=property.id) }}" 
         class="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition-all text-sm w-full sm:w-auto">
        Agendar Visita
      </a>

      <!-- Enviar mensaje por WhatsApp -->
      <a href="https://wa.me/?text=Estoy%20interesado%20en%20la%20propiedad%20{{ property.id }}" 
         target="_blank" 
         class="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 transition-all text-sm w-full sm:w-auto">
        Enviar WhatsApp
      </a>

      <!-- Comprar -->
      <a href="{{ url_for('main.buy_property', property_id=property.id) }}" 
         class="bg-yellow-500 text-white px-6 py-2 rounded-md hover:bg-yellow-600 transition-all text-sm w-full sm:w-auto">
        Comprar
      </a>
    </div>
  </main>

</body>
</html>
