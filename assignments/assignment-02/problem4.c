int foo(int n) {
  int result = 0; // This is the 'local_c = 0' part

  switch (n) {
    case 1:
      result = 1;
      break;
    case 2:
      result = 2;
      break;
    case 3:
      result = 3;
      break;
    case 4:
      result = 4;
      break;
    default:
      // If n is not 1, 2, 3, or 4,
      // 'result' just stays 0.
      break;
  }

  return result;
}