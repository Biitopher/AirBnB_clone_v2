#!/usr/bin/env bash
#Using Puupet to set up web servers

# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
  <head>
  </head>
  <body>
    <p>Test Page</p>
  </body>
</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create or recreate symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  notify => Service['nginx'],
}

# Manage Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "location /hbnb_static {
    alias /data/web_static/current/;
    index index.html;
}\n",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure => running,
  enable => true,
}
