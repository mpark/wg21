#include <memory>
#include <variant>

struct Expr;
struct Neg { std::shared_ptr<Expr> expr; };
struct Add { std::shared_ptr<Expr> lhs, rhs; };
struct Mul { std::shared_ptr<Expr> lhs, rhs; };
struct Expr : std::variant<int, Neg, Add, Mul> { using variant::variant; };

namespace std {
    template <>
    struct variant_size<Expr> : variant_size<Expr::variant> {};

    template <std::size_t I>
    struct variant_alternative<I, Expr> : variant_alternative<I, Expr::variant> {};
}

int eval(const Expr& expr) {
  struct visitor {
    int operator()(int i) const {
      return i;
    }
    int operator()(const Neg& n) const {
      return -eval(*n.expr);
    }
    int operator()(const Add& a) const {
      return eval(*a.lhs) + eval(*a.rhs);
    }
    int operator()(const Mul& m) const {
      // Optimize for multiplication by 0
      if(int * lhsInt = std::get_if<int>(m.lhs.get()); lhsInt && *lhsInt == 0)
        return 0;
      if(int * rhsInt = std::get_if<int>(m.rhs.get()); rhsInt && *rhsInt == 0)
        return 0;

      return eval(*m.lhs) * eval(*m.rhs);
    }
  };
  return std::visit(visitor{}, expr);
}

enum Color { R, B };

template<typename T>
struct Tree;

struct Empty { };

template<typename T>
struct Valued {
  Color c;
  std::shared_ptr<Tree<T>> lhs;
  T value;
  std::shared_ptr<Tree<T>> rhs;
};

template<typename T>
struct Tree : std::variant<Empty, Valued<T>> {
  using std::variant<Empty, Valued<T>>::variant;
};


template<typename T>
Tree<T> balance(Color c, Tree<T> lhs, T value, Tree<T> rhs) {
  if(c == B) {
    // case 1
    if(Valued<T> * lhsValued = std::get_if<Valued<T>>(&lhs);
       lhsValued && lhsValued->c == R)
    {
      // case 1.a
      if(Valued<T> * lhsLhsValued = std::get_if<Valued<T>>(lhsValued->lhs.get());
         lhsLhsValued && lhsLhsValued->c == R)
      {
          return Valued<T>{
            R,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhsLhsValued->lhs,
              lhsLhsValued->value,
              lhsLhsValued->rhs}),
            lhsValued->value,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhsValued->rhs,
              value,
              std::make_shared<Tree<T>>(rhs)})};
      }
      // case 1.b
      if(Valued<T> * lhsRhsValued = std::get_if<Valued<T>>(lhsValued->rhs.get());
         lhsRhsValued && lhsRhsValued->c == R)
      {
          return Valued<T>{
            R,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhsValued->lhs,
              lhsValued->value,
              lhsRhsValued->lhs}),
            lhsRhsValued->value,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhsRhsValued->rhs,
              value,
              std::make_shared<Tree<T>>(rhs)})};
      }
    }
    // case 2
    if(Valued<T> * rhsValued = std::get_if<Valued<T>>(&rhs);
       rhsValued && rhsValued->c == R)
    {
      // case 2.a
      if(Valued<T> * rhsLhsValued = std::get_if<Valued<T>>(rhsValued->lhs.get());
         rhsLhsValued && rhsLhsValued->c == R)
      {
          return Valued<T>{
            R,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              std::make_shared<Tree<T>>(lhs),
              value,
              rhsLhsValued->lhs}),
            rhsLhsValued->value,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              rhsLhsValued->rhs,
              rhsValued->value,
              rhsValued->rhs})};
      }

      // case 2.b
      if(Valued<T> * rhsRhsValued = std::get_if<Valued<T>>(rhsValued->rhs.get());
         rhsRhsValued && rhsRhsValued->c == R)
      {
          return Valued<T>{
            R,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              std::make_shared<Tree<T>>(lhs),
              value,
              rhsValued->lhs}),
            rhsValued->value,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              rhsRhsValued->lhs,
              rhsRhsValued->value,
              rhsRhsValued->rhs})};
      }
    }
  }
  return Valued<T>{c, std::make_shared<Tree<T>>(lhs), value, std::make_shared<Tree<T>>(rhs)};
}

template<typename T>
Tree<T> balance2(Color c, std::shared_ptr<Tree<T>> lhs, T value, std::shared_ptr<Tree<T>> rhs) {
  if(c == B) {
    // case 1
    if(Valued<T> * lhsValued = std::get_if<Valued<T>>(lhs.get());
       lhsValued && lhsValued->c == R)
    {
      // case 1.a
      if(Valued<T> * lhsLhsValued = std::get_if<Valued<T>>(lhsValued->lhs.get());
         lhsLhsValued && lhsLhsValued->c == R)
      {
          return Valued<T>{
            R,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhsLhsValued->lhs,
              lhsLhsValued->value,
              lhsLhsValued->rhs}),
            lhsValued->value,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhsValued->rhs,
              value,
              rhs})};
      }
      // case 1.b
      if(Valued<T> * lhsRhsValued = std::get_if<Valued<T>>(lhsValued->rhs.get());
         lhsRhsValued && lhsRhsValued->c == R)
      {
          return Valued<T>{
            R,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhsValued->lhs,
              lhsValued->value,
              lhsRhsValued->lhs}),
            lhsRhsValued->value,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhsRhsValued->rhs,
              value,
              rhs})};
      }
    }
    // case 2
    if(Valued<T> * rhsValued = std::get_if<Valued<T>>(rhs.get());
       rhsValued && rhsValued->c == R)
    {
      // case 2.a
      if(Valued<T> * rhsLhsValued = std::get_if<Valued<T>>(rhsValued->lhs.get());
         rhsLhsValued && rhsLhsValued->c == R)
      {
          return Valued<T>{
            R,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhs,
              value,
              rhsLhsValued->lhs}),
            rhsLhsValued->value,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              rhsLhsValued->rhs,
              rhsValued->value,
              rhsValued->rhs})};
      }

      // case 2.b
      if(Valued<T> * rhsRhsValued = std::get_if<Valued<T>>(rhsValued->rhs.get());
         rhsRhsValued && rhsRhsValued->c == R)
      {
          return Valued<T>{
            R,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              lhs,
              value,
              rhsValued->lhs}),
            rhsValued->value,
            std::make_shared<Tree<T>>(Valued<T>{
              B,
              rhsRhsValued->lhs,
              rhsRhsValued->value,
              rhsRhsValued->rhs})};
      }
    }
  }
  return Valued<T>{c, lhs, value, rhs};
}

/*
template<typename T>
Tree<T> balance(Color c, std::shared_ptr<Tree<T>> lhs, T value, std::shared_ptr<Tree<T>> rhs) {
  using V = Valued<T>;
  return inspect(c,lhs,value,rhs) {
    [^B, *<V> [^R, *<V> [^R, a, x, b], y, c], z, d] => V{R,
                                                         std::make_shared<Tree<T>>(V{B, a, x, b},
                                                         y,
                                                         std::make_shared<Tree<T>>(V{B, c, z, d}},
    [^B, *<V> [^R, a, x, *<V> [^R, b, y, c]], z, d] => V{R,
                                                         std::make_shared<Tree<T>>(V{B, a, x, b},
                                                         y,
                                                         std::make_shared<Tree<T>>(V{B, c, z, d}},
    [^B, a, x, *<V> [^R, *<V> [^R, b, y, c], z, d]] => V{R,
                                                         std::make_shared<Tree<T>>(V{B, a, x, b},
                                                         y,
                                                         std::make_shared<Tree<T>>(V{B, c, z, d}},
    [^B, a, x, *<V> [^R, b, y, *<V> [^R, c, z, d]]] => V{R,
                                                         std::make_shared<Tree<T>>(V{B, a, x, b},
                                                         y,
                                                         std::make_shared<Tree<T>>(V{B, c, z, d}},
    [color, a, x, b]                                => V{color, a, x, b}
  };
}
*/


//data Color = R | B
//data Tree elt = E | T Color (Tree elt) elt (Tree elt)
//
//balance B (T R (T R a x b) y c) z d = T R (T B a x b) y (T B c z d)
//balance B (T R a x (T R b y c)) z d = T R (T B a x b) y (T B c z d)
//balance B a x (T R (T R b y c) z d) = T R (T B a x b) y (T B c z d)
//balance B a x (T R b y (T R c z d)) = T R (T B a x b) y (T B c z d)
//balance color a x b = T color a x b


int main() 
{
  balance(R, *(Tree<int>*)0, 3, *(Tree<int>*)0);
  balance2(R, std::shared_ptr<Tree<int>>(), 3, std::shared_ptr<Tree<int>>());
}
