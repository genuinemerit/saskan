#!/bin/bash
mongo << EOF
    use admin
    db.createUser( { user: 'bowadmin',
                     pwd: 'sdf9087ADJ',
                     roles: [ { role: "userAdminAnyDatabase", db: "admin"} ] } );
EOF
