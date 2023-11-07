const UserList = (msg) => {
  if (msg.payload.mensaje.length == 0) return <> No hay Jugadores actualmente </>
  

  const userList = msg.payload.mensaje.map(user => 
  <li key={user.id} > {user.name} </li>
  )
  return (
      <ul>
        {userList}
      </ul>
  );
};

export default UserList;