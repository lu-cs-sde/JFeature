// 0
// Reflection

import java.lang.Class;
import java.lang.reflect.*;

class A {
  void foo() {
    A a = new A();
    Class obj = a.getClass();
    String name = obj.getName();
    int modifier = obj.getModifiers();
  }
}